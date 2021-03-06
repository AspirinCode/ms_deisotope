# pragma: no cover
import re
import warnings
from collections import OrderedDict, defaultdict

import logging

import numpy as np

from ms_deisotope.data_source.common import (
    ScanDataSource, RandomAccessScanSource,
    Scan, PrecursorInformation, ChargeNotProvided,
    ActivationInformation, IsolationWindow,
    ScanAcquisitionInformation, ScanEventInformation, ScanWindow,
    component, ComponentGroup, InstrumentInformation,
    FileInformation, MultipleActivationInformation, ScanFileMetadataBase)
from .metadata.activation import (supplemental_term_map, dissociation_methods_map)
from .metadata.file_information import (MS_MS1_Spectrum, MS_MSn_Spectrum)
from ms_deisotope.utils import Base


try:
    from ms_deisotope.data_source._vendor.MSFileReader import (
        ThermoRawfile as _ThermoRawFileAPI, register_dll,
        log as _api_logger)

    comtypes_logger = logging.getLogger("comtypes")
    comtypes_logger.setLevel("INFO")
    _api_logger.setLevel("INFO")

    def is_thermo_raw_file(path):
        try:
            _ThermoRawFileAPI(path)
            return True
        except (WindowsError, IOError, ImportError):
            return False

    def infer_reader(path):
        if is_thermo_raw_file(path):
            return ThermoRawLoader
        raise ValueError("Not Thermo Raw File")

    def determine_if_available():
        try:
            _ThermoRawFileAPI.create_com_object()
            return True
        except ImportError:
            return False
except ImportError as e:  # pragma: no cover
    message = str(e)

    def is_thermo_raw_file(path):
        return False

    def infer_reader(path):
        raise ValueError(message)

    def register_dll(paths):
        try:
            warnings.warn("no-op: %s" % (message,))
        except Exception:
            pass
        return False

    def determine_if_available():
        try:
            warnings.warn("no-op: %s" % (message,))
        except Exception:
            pass
        return False

try:
    range = xrange
except NameError:
    pass


analyzer_pat = re.compile(r"(?P<mass_analyzer_type>ITMS|TQMS|SQMS|TOFMS|FTMS|SECTOR)")
polarity_pat = re.compile(r"(?P<polarity>[\+\-])")
point_type_pat = re.compile(r"(?P<point_type>[CP])")
ionization_pat = re.compile(r"(?P<ionization_type>EI|CI|FAB|APCI|ESI|APCI|NSI|TSP|FD|MALDI|GD)")
scan_type_pat = re.compile(r"(?P<scan_type>FULL|SIM|SRM|CRM|Z|Q1MS|Q3MS)")
ms_level_pat = re.compile(r" ms(?P<level>\d*) ")
activation_pat = re.compile(
    r"""(?:(?P<isolation_mz>\d+\.\d*)@
        (?P<activation_type>[a-z]+)
        (?P<activation_energy>\d*\.?\d*))""", re.VERBOSE)
activation_mode_pat = re.compile(
    r"""(?P<activation_type>[a-z]+)
        (?P<activation_energy>\d*\.\d*)""", re.VERBOSE)
scan_window_pat = re.compile(
    r"""
    \[(?P<scan_start>[0-9\.]+)-(?P<scan_end>[0-9\.]+)\]
    """, re.VERBOSE)

analyzer_map = {
    'FTMS': component("orbitrap"),
    "ITMS": component("ion trap"),
    "SQMS": component("quadrupole"),
    "TQMS": component("quadrupole"),
    "TOFMS": component("time-of-flight"),
    "SECTOR": component("magnetic sector")
}


ionization_map = {
    "EI": component("electron ionization"),
    "CI": component("chemical ionization"),
    "FAB": component("fast atom bombardment ionization"),
    "ESI": component("electrospray ionization"),
    "NSI": component("nanoelectrospray"),
    "APCI": component("atmospheric pressure chemical ionization"),
    "TSP": component("thermospray ionization"),
    "FD": component("field desorption"),
    "MALDI": component("matrix assisted laser desorption ionization"),
    "GD": component("glow discharge ionization"),
}


inlet_map = {
    "FAB": component("continuous flow fast atom bombardment"),
    "ESI": component("electrospray inlet"),
    "NSI": component("nanospray inlet"),
    "TSP": component("thermospray inlet"),
}


class FilterString(str):
    def __init__(self, value):
        self.data = self._parse()

    def get(self, key):
        return self.data.get(key)

    def _parse(self):
        return filter_string_parser(self)


def filter_string_parser(line):
    """Parses instrument information from Thermo's filter string

    Parameters
    ----------
    line : str
        The filter string associated with a scan

    Returns
    -------
    dict
        Fields extracted from the filter string
    """
    words = line.upper().split(" ")
    values = dict()
    i = 0
    values['supplemental_activation'] = " sa " in line
    ms_level_info = ms_level_pat.search(line)
    if ms_level_info is not None:
        ms_level_data = ms_level_info.groupdict()
        level = ms_level_data.get("level")
        if level != "":
            parts = line[ms_level_info.end():].split(" ")
            tandem_sequence = []
            for part in parts:
                activation_info = activation_pat.search(part)
                if activation_info is not None:
                    activation_info = activation_info.groupdict()
                    activation_event = dict()
                    activation_event["isolation_mz"] = float(activation_info['isolation_mz'])
                    activation_event["activation_type"] = [activation_info['activation_type']]
                    activation_event["activation_energy"] = [float(activation_info['activation_energy'])]
                    if part.count("@") > 1:
                        act_events = activation_mode_pat.finditer(part)
                        # discard the first match which we already recorded
                        next(act_events)
                        for match in act_events:
                            act_type, act_energy = match.groups()
                            act_energy = float(act_energy)
                            activation_event["activation_type"].append(act_type)
                            activation_event['activation_energy'].append(act_energy)
                    tandem_sequence.append(activation_event)
            values['ms_level'] = int(level)
            values['tandem_sequence'] = tandem_sequence

    scan_window_info = scan_window_pat.search(line)
    if scan_window_info is not None:
        values['scan_window'] = (float(scan_window_info.group(1)), float(scan_window_info.group(2)))

    try:
        word = words[i]
        i += 1
        analyzer_info = analyzer_pat.search(word)
        if analyzer_info is not None:
            values['analyzer'] = analyzer_info.group(0)
            word = words[i]
            i += 1
        polarity_info = polarity_pat.search(word)
        if polarity_info is not None:
            polarity_sigil = polarity_info.group(0)
            if polarity_sigil == "+":
                polarity = 1
            elif polarity_sigil == "-":
                polarity = -1
            else:
                polarity = 0
            values["polarity"] = polarity
            word = words[i]
            i += 1
        if word in "PC":
            if word == 'P':
                values['peak_mode'] = 'profile'
            else:
                values['peak_mode'] = 'centroid'
            word = words[i]
            i += 1
        ionization_info = ionization_pat.search(word)
        if ionization_info is not None:
            values['ionization'] = ionization_info.group(0)
            word = words[i]
            i += 1

        return values
    except IndexError:
        return values


_id_template = "controllerType=0 controllerNumber=1 scan="


class _RawFileMetadataLoader(ScanFileMetadataBase):
    def _build_scan_type_index(self):
        self.make_iterator(grouped=False)
        index = defaultdict(int)
        analyzer_counter = 1
        analyzer_confs = dict()
        for scan in self:
            index[scan.ms_level] += 1
            fline = self._filter_string(scan._data)
            analyzer = analyzer_map[fline.data['analyzer']]
            try:
                analyzer_confs[analyzer]
            except KeyError:
                analyzer_confs[analyzer] = analyzer_counter
                analyzer_counter += 1
        self.reset()
        self._scan_type_index = index
        self._analyzer_to_configuration_index = analyzer_confs

    def _get_instrument_info(self):
        scan = self.get_scan_by_index(0)
        filter_string = self._filter_string(scan._data)
        ionization_label = filter_string.data.get("ionization")
        try:
            ionization = ionization_map[ionization_label]
        except KeyError:
            ionization = ionization_map['ESI']
        try:
            inlet = inlet_map[ionization_label]
        except KeyError:
            inlet = None

        source_group = ComponentGroup("source", [], 1)
        source_group.add(ionization)
        if inlet is not None:
            source_group.add(inlet)
        configs = []
        for analyzer, counter in sorted(self._analyzer_to_configuration_index.items(), key=lambda x: x[1]):
            analyzer_group = ComponentGroup('analyzer', [analyzer], 2)
            configs.append(InstrumentInformation(counter, [source_group, analyzer_group]))
        self._instrument_config = {
            c.id: c for c in configs
        }
        return configs

    def instrument_configuration(self):
        return sorted(self._instrument_config.values(), key=lambda x: x.id)

    def file_description(self):
        fi = FileInformation({}, [])
        fi.add_file(self.source_file)
        sf = fi.source_files[0]
        sf.add_checksum("sha1")
        if 1 in self._scan_type_index:
            fi.add_content(MS_MS1_Spectrum)
        scan_types = sorted(self._scan_type_index, reverse=True)
        if scan_types:
            if scan_types[0] > 1:
                fi.add_content(MS_MSn_Spectrum)
        return fi

    def data_processing(self):
        return []


class _InstrumentMethod(object):
    def __init__(self, method_text):
        self.text = method_text
        (self.isolation_width_by_segment_and_event,
         self.isolation_width_by_segment_and_ms_level) = method_parser(self.text)

    def isolation_width_for(self, segment, event=None, ms_level=None):
        if event is not None:
            try:
                width = self.isolation_width_by_segment_and_event[segment][event]
                return width
            except KeyError:
                return 0.0
        elif ms_level is not None:
            try:
                width = self.isolation_width_by_segment_and_ms_level[segment][ms_level]
                return width
            except KeyError:
                return 0.0
        else:
            raise ValueError("One of event or ms_level must not be None!")


def method_parser(method_text):
    scan_segment_re = re.compile(r"\s*Segment (\d+) Information\s*")
    scan_event_re = re.compile(r"\s*(\d+):.*")
    scan_event_isolation_width_re = re.compile(r"\s*Isolation Width:\s*(\S+)\s*")
    scan_event_iso_w_re = re.compile(r"\s*MS.*:.*\s+IsoW\s+(\S+)\s*")
    repeated_event_re = re.compile(r"\s*Scan Event (\d+) repeated for top (\d+)\s*")
    default_isolation_width_re = re.compile(r"\s*MS(\d+) Isolation Width:\s*(\S+)\s*")

    scan_segment = 1
    scan_event = 0
    scan_event_details = False
    data_dependent_settings = False

    isolation_width_by_segment_and_event = defaultdict(dict)
    isolation_width_by_segment_and_ms_level = defaultdict(dict)

    for line in method_text.splitlines():
        match = scan_segment_re.match(line)

        if match:
            scan_segment = int(match.group(1))
            continue

        if "Scan Event Details" in line:
            scan_event_details = True
            continue

        if scan_event_details:
            match = scan_event_re.match(line)
            if match:
                scan_event = int(match.group(1))
                continue

            match = scan_event_isolation_width_re.match(line)
            if match:
                isolation_width_by_segment_and_event[scan_segment][scan_event] = float(match.group(1))
                continue

            match = scan_event_iso_w_re.match(line)
            if match:
                isolation_width_by_segment_and_event[scan_segment][scan_event] = float(match.group(1))
                continue

            match = repeated_event_re.match(line)
            if match:
                repeated_event = int(match.group(1))
                repeat_count = int(match.group(2))
                repeated_width = isolation_width_by_segment_and_event[scan_segment][repeated_event]
                for i in range(repeated_width + 1, repeat_count + repeated_width):
                    isolation_width_by_segment_and_event[scan_segment][i] = repeated_width
                continue

            if not line.strip():
                scan_event_details = False

        if "Data Dependent Settings" in line:
            data_dependent_settings = True
            continue

        if data_dependent_settings:
            match = default_isolation_width_re.match(line)
            if match:
                ms_level = int(match.group(1))
                width = float(match.group(2))
                isolation_width_by_segment_and_ms_level[scan_segment][ms_level] = width
                continue

            if not line.strip():
                data_dependent_settings = False

    return isolation_width_by_segment_and_event, isolation_width_by_segment_and_ms_level


class ThermoRawScanPtr(Base):
    def __init__(self, scan_number):
        self.scan_number = scan_number
        self.filter_string = None

    def validate(self, source):
        try:
            source._scan_time(self)
            return True
        except IOError:
            return False


def _make_id(scan_number):
    try:
        return "%s%d" % (_id_template, (scan_number))
    except TypeError:
        return None


def _parse_id(scan_id):
    return int(scan_id.replace(_id_template, ""))


class ThermoRawDataInterface(ScanDataSource):
    def _scan_index(self, scan):
        return scan.scan_number - 1

    def _scan_id(self, scan):
        return _make_id(scan.scan_number)

    def _scan_time(self, scan):
        return self._source.RTFromScanNum(
            scan.scan_number)

    def _ms_level(self, scan):
        return self._source.GetMSOrderForScanNum(
            scan.scan_number)

    def _is_profile(self, scan):
        return self._source.IsProfileScanForScanNum(
            scan.scan_number)

    def _polarity(self, scan):
        filter_string = self._filter_string(scan)
        return filter_string.data['polarity']

    def _filter_string(self, scan):
        if scan.filter_string is None:
            scan.filter_string = FilterString(self._source.GetFilterForScanNum(scan.scan_number))
        return scan.filter_string

    def _scan_title(self, scan):
        return "%s %r" % (self._scan_id(scan), self._filter_string(scan))

    def _scan_arrays(self, scan):
        arrays, flags = self._source.GetMassListFromScanNum(
            scan.scan_number)
        mz, intensity = arrays
        return np.array(mz), np.array(intensity)

    def _precursor_information(self, scan):
        if self._ms_level(scan) == 1:
            return None
        scan_number = scan.scan_number
        pinfo_struct = self._source.GetPrecursorInfoFromScanNum(scan_number)
        precursor_scan_number = None
        labels, flags, _ = self._source.GetAllMSOrderData(scan_number)
        if pinfo_struct:
            # this struct field is unreliable and may fall outside the
            # isolation window
            mz = pinfo_struct.monoIsoMass
            charge = pinfo_struct.chargeState
            intensity = float(labels.intensity[0])
            # this struct field is unreliable, and simple to infer
            # precursor_scan_number = pinfo_struct.scanNumber + 1
        else:
            mz = labels.mass[0]
            intensity = float(labels.intensity[0])
            charge = labels.charge[0]
        if not charge:
            charge = ChargeNotProvided
        trailer = self._source.GetTrailerExtraForScanNum(scan_number)
        _mz = trailer.get('Monoisotopic M/Z', 0.0)
        # prefer the trailer m/z if available?
        if _mz > 0:
            mz = _mz

        # imitate proteowizard's firmware bug correction
        isolation_window = self._isolation_window(scan)
        if (isolation_window.upper + isolation_window.lower) / 2 <= 2.0:
            if (isolation_window.target - 3.0 > mz) or (isolation_window.target + 2.5 < mz):
                mz = isolation_window.target
        elif mz not in isolation_window:
            mz = isolation_window.target
        _charge = trailer.get('Charge State', 0)
        if _charge != 0:
            charge = _charge
        # Guess which previous scan was the precursor by iterating
        # backwards until a scan is found with a lower MS level
        if precursor_scan_number is None:
            last_index = self._scan_index(scan) - 1
            current_level = self._ms_level(scan)
            i = 0
            while last_index >= 0 and i < 100:
                prev_scan = self.get_scan_by_index(last_index)
                if prev_scan.ms_level >= current_level:
                    last_index -= 1
                else:
                    precursor_scan_number = prev_scan._data.scan_number
                    break
                i += 1
        if intensity is None:
            intensity = 0.0
        if mz is None:
            mz = 0.0
        if charge is None or charge == 0:
            charge = ChargeNotProvided
        pinfo = PrecursorInformation(
            mz, intensity, charge, _make_id(precursor_scan_number),
            source=self,
            product_scan_id=_make_id(scan.scan_number))
        return pinfo

    def _activation(self, scan):
        filter_string = self._filter_string(scan)
        tandem_sequence = filter_string.get("tandem_sequence")
        # If the tandem sequence exists, the last entry is the most recent tandem acquisition.
        # It will list contain one or more activation types. Alternatively, multiple activations
        # of the same precursor may exist in the list as separate events in the tandem sequence.
        if tandem_sequence is not None:
            activation_event = tandem_sequence[-1]
            activation_type = list(activation_event.get("activation_type"))
            has_supplemental_activation = filter_string.get("supplemental_activation")

            if activation_type is not None:
                energy = list(activation_event.get("activation_energy"))
                if len(tandem_sequence) > 1:
                    prev_event = tandem_sequence[-2]
                    # Merge previous tandem sequences of the same precursor
                    if abs(prev_event['isolation_mz'] - activation_event['isolation_mz']) < 1e-3:
                        activation_type = list(prev_event.get("activation_type")) + activation_type
                        energy = list(prev_event.get("activation_energy")) + energy
                        has_supplemental_activation = True

                if has_supplemental_activation and len(activation_type) > 1:
                    activation_type.append(supplemental_term_map[
                        dissociation_methods_map[activation_type[-1]]])
                if len(activation_type) == 1:
                    return ActivationInformation(activation_type[0], energy[0])
                else:
                    return MultipleActivationInformation(activation_type, energy)
        return None

    def _get_scan_segment(self, scan):
        trailer = self._source.GetTrailerExtraForScanNum(scan.scan_number)
        try:
            return int(trailer['Scan Segment'])
        except KeyError:
            return 1

    def _get_scan_event(self, scan):
        trailer = self._source.GetTrailerExtraForScanNum(scan.scan_number)
        try:
            return int(trailer['Scan Event'])
        except KeyError:
            return 1

    def _isolation_window(self, scan):
        ms_level = self._ms_level(scan)
        if ms_level == 1:
            return None
        isolation_width = 0
        trailer = self._source.GetTrailerExtraForScanNum(scan.scan_number)
        try:
            isolation_width = trailer['MS%d Isolation Width' % ms_level]
        except KeyError:
            segment = self._get_scan_segment(scan)
            event = self._get_scan_event(scan)
            isolation_width = self._method.isolation_width_for(segment, event=event)
            if not isolation_width:
                isolation_width = self._method.isolation_width_for(segment, ms_level=ms_level)
        if isolation_width == 0:
            return None
        isolation_width /= 2.
        isolation_mz = self._source.GetPrecursorMassForScanNum(scan.scan_number, ms_level)
        return IsolationWindow(isolation_width, isolation_mz, isolation_width)

    def _instrument_configuration(self, scan):
        fline = self._filter_string(scan)
        try:
            confid = self._analyzer_to_configuration_index[analyzer_map[fline.data.get("analyzer")]]
            return self._instrument_config[confid]
        except KeyError:
            return None

    def _acquisition_information(self, scan):
        fline = self._filter_string(scan)

        event = ScanEventInformation(
            self._scan_time(scan),
            window_list=[ScanWindow(
                fline.get("scan_window")[0], fline.get("scan_window")[1])])
        return ScanAcquisitionInformation("no combination", [event])

    def _annotations(self, scan):
        fline = self._filter_string(scan)
        trailer_extras = self._source.GetTrailerExtraForScanNum(scan.scan_number)
        annots = {
            "filter_string": fline,
        }
        microscans = trailer_extras.get("Micro Scan Count")
        if microscans is not None:
            annots['[Thermo Trailer Extra]Micro Scan Count'] = microscans
        scan_segment = trailer_extras.get("Scan Segment")
        if scan_segment is not None:
            annots['[Thermo Trailer Extra]Scan Segment'] = scan_segment
        scan_event = trailer_extras.get("Scan Event")
        if scan_event is not None:
            annots['[Thermo Trailer Extra]Scan Event'] = scan_event
        mono_mz = trailer_extras.get("Monoisotopic M/Z")
        if mono_mz is not None and mono_mz > 0:
            annots['[Thermo Trailer Extra]Monoisotopic M/Z'] = mono_mz
        hcd_ev = trailer_extras.get('HCD Energy eV')
        if hcd_ev is not None and hcd_ev > 0:
            annots['[Thermo Trailer Extra]HCD Energy eV'] = hcd_ev
        return annots


class ThermoRawLoader(ThermoRawDataInterface, RandomAccessScanSource, _RawFileMetadataLoader):
    def __init__(self, source_file, _load_metadata=True, **kwargs):
        self.source_file = source_file
        self._source = _ThermoRawFileAPI(self.source_file)
        self._producer = None
        self._scan_type_index = dict()
        self.make_iterator()
        self.initialize_scan_cache()
        self._index = self._pack_index()
        self._first_scan_time = self.get_scan_by_index(0).scan_time
        self._last_scan_time = self.get_scan_by_id(self._source.LastSpectrumNumber).scan_time
        if _load_metadata:
            self._method = self._parse_method()
            self._build_scan_type_index()
            self._get_instrument_info()

    def _parse_method(self):
        return _InstrumentMethod(self._source.GetInstMethod())

    def _has_ms1_scans(self):
        if self._scan_type_index:
            return 1 in self._scan_type_index
        else:
            # metadata has not been loaded so best to assume there is
            return True

    def _has_msn_scans(self):
        if self._scan_type_index:
            return max(self._scan_type_index) > 1
        else:
            # metadata has not been loaded so best to assume there is
            return True

    def has_msn_scans(self):
        return self._has_msn_scans()

    def has_ms1_scans(self):
        return self._has_ms1_scans()

    def __reduce__(self):
        return self.__class__, (self.source_file, False)

    @property
    def index(self):
        return self._index

    def __repr__(self):
        return "ThermoRawLoader(%r)" % (self.source_file)

    def _pack_index(self):
        index = OrderedDict()
        for sn in range(1, self._source.NumSpectra + 1):
            index[_make_id(sn)] = sn
        return index

    def __len__(self):
        return len(self.index)

    def close(self):
        if self._source is not None:
            self._source.Close()
            self._source = None

    def __del__(self):
        self.close()

    def reset(self):
        self.make_iterator(None)
        self.initialize_scan_cache()

    def _scan_time_to_scan_number(self, scan_time):
        scan_number = self._source.ScanNumFromRT(scan_time)
        return scan_number

    def get_scan_by_id(self, scan_id):
        """Retrieve the scan object for the specified scan id.

        If the scan object is still bound and in memory somewhere,
        a reference to that same object will be returned. Otherwise,
        a new object will be created.

        Parameters
        ----------
        scan_id : str
            The unique scan id value to be retrieved

        Returns
        -------
        Scan
        """
        scan_number = int(str(scan_id).replace(_id_template, ''))
        try:
            return self._scan_cache[scan_number]
        except KeyError:
            package = ThermoRawScanPtr(scan_number)
            if not package.validate(self):
                raise KeyError(str(scan_id))
            scan = Scan(package, self)
            self._scan_cache[scan_number] = scan
            return scan

    def get_scan_by_index(self, index):
        """Retrieve the scan object for the specified scan index.

        This internally calls :meth:`get_scan_by_id` which will
        use its cache.

        Parameters
        ----------
        index: int
            The index to get the scan for

        Returns
        -------
        Scan
        """
        scan_number = int(index) + 1
        try:
            return self._scan_cache[scan_number]
        except KeyError:
            package = ThermoRawScanPtr(scan_number)
            if not package.validate(self):
                raise KeyError(index)
            scan = Scan(package, self)
            self._scan_cache[scan_number] = scan
            return scan

    def get_scan_by_time(self, time):
        """Retrieve the scan object for the specified scan time.

        This internally calls :meth:`get_scan_by_id` which will
        use its cache.

        Parameters
        ----------
        time : float
            The time to get the nearest scan from

        Returns
        -------
        Scan
        """
        if time < self._first_scan_time:
            time = self._first_scan_time
        elif time > self._last_scan_time:
            time = self._last_scan_time
        scan_number = self._scan_time_to_scan_number(time)
        try:
            return self._scan_cache[scan_number]
        except KeyError:
            package = ThermoRawScanPtr(scan_number)
            scan = Scan(package, self)
            self._scan_cache[scan_number] = scan
            return scan

    def start_from_scan(self, scan_id=None, rt=None, index=None, require_ms1=True, grouped=True):
        '''Reconstruct an iterator which will start from the scan matching one of ``scan_id``,
        ``rt``, or ``index``. Only one may be provided.

        After invoking this method, the iterator this object wraps will be changed to begin
        yielding scan bunchs (or single scans if ``grouped`` is ``False``).

        Arguments
        ---------
        scan_id: str, optional
            Start from the scan with the specified id.
        rt: float, optional
            Start from the scan nearest to specified time (in minutes) in the run. If no
            exact match is found, the nearest scan time will be found, rounded up.
        index: int, optional
            Start from the scan with the specified index.
        require_ms1: bool, optional
            Whether the iterator must start from an MS1 scan. True by default.
        grouped: bool, optional
            whether the iterator should yield scan bunches or single scans. True by default.
        '''
        if scan_id is not None:
            scan_number = int(str(scan_id).replace(_id_template, '')) - 1
        elif index is not None:
            scan_number = int(index)
        elif rt is not None:
            scan_number = self._scan_time_to_scan_number(rt)
        if require_ms1:
            start_index = scan_number
            while start_index != 0:
                scan = self.get_scan_by_index(start_index)
                if scan.ms_level > 1:
                    start_index -= 1
                else:
                    break
            scan_number = start_index
        iterator = self._make_pointer_iterator(start_index=scan_number)
        if grouped:
            self._producer = self._scan_group_iterator(iterator)
        else:
            self._producer = self._single_scan_iterator(iterator)
        return self

    def _make_scan_index_producer(self, start_index=None, start_time=None):
        if start_index is not None:
            return range(start_index + 1, self._source.NumSpectra + 1)
        elif start_time is not None:
            start_index = self._scan_time_to_scan_number(start_time)
            while start_index != 1:
                scan = self.get_scan_by_index(start_index)
                if scan.ms_level > 1:
                    start_index -= 1
                else:
                    break
            return range(start_index, self._source.NumSpectra + 1)
        else:
            return range(1, self._source.NumSpectra + 1)

    def _make_pointer_iterator(self, start_index=None, start_time=None):
        iterator = self._make_scan_index_producer(start_index, start_time)
        for i in iterator:
            yield ThermoRawScanPtr(i)

    def _make_default_iterator(self):
        return self._make_pointer_iterator()

    def _make_cache_key(self, scan):
        return scan._data.scan_number

    def next(self):
        return next(self._producer)
