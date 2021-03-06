# -*- coding: utf-8 -*-

from collections import defaultdict
from brainpy import (
    calculate_mass, neutral_mass, PROTON,
    isotopic_variants, mass_charge_ratio)

from brainpy.composition import (
    parse_formula,
    PyComposition)

from .utils import dict_proxy


class TheoreticalIsotopicPattern(object):
    """Represent a theoretical isotopic peak list

    Attributes
    ----------
    peaklist: list of :class:`~.brainpy.TheoreticalPeak`
        The theoretical isotopic pattern peak list
    origin: float
        The monoisotopic peak's m/z
    """

    def __init__(self, peaklist, origin, offset=None):
        self.peaklist = list(peaklist)
        self.origin = float(origin)
        if offset is None:
            offset = self.peaklist[0].mz - origin
        self.offset = float(offset)

    def get(self, i):
        return self.peaklist[i]

    def __len__(self):
        return len(self.peaklist)

    def __getitem__(self, i):
        return self.peaklist[i]

    def __iter__(self):
        return iter(self.peaklist)

    def __reduce__(self):
        return self.__class__, (self.peaklist, self.origin, self.offset)

    def clone(self):
        return self.__class__([p.clone() for p in self.peaklist], self.origin, self.offset)

    def truncate_after(self, truncate_after=0.95):
        """Drops peaks from the end of the isotopic pattern
        which make up the last ``1 - truncate_after`` percent
        of the isotopic pattern.

        After truncation, the pattern is renormalized to sum to ``1``

        Parameters
        ----------
        truncate_after : float, optional
            The percentage of the isotopic pattern signal to retain. Defaults
            to 0.95.

        Returns
        -------
        TheoreticalIsotopicPattern
            self
        """
        cumsum = 0
        result = []
        n = len(self)
        for i in range(n):
            peak = self[i]
            cumsum += peak.intensity
            result.append(peak)
            if cumsum >= truncate_after:
                break
        self.peaklist = result
        n = len(self)
        normalizer = 1. / cumsum
        for i in range(n):
            peak = self[i]
            peak.intensity *= normalizer
        return self

    def shift(self, offset):
        """Shift all the m/z of peaks in the isotopic pattern by ``offset``
        m/z.

        This will update :attr:`origin` to reflect the new starting
        monoisotopic m/z.

        Parameters
        ----------
        offset : float
            The amount to shift each peak in the pattern by in m/z

        Returns
        -------
        TheoreticalIsotopicPattern
            self
        """
        new_origin = offset
        delta = (new_origin - self.origin)
        self.origin = new_origin
        for peak in self.peaklist:
            peak.mz += delta
        return self

    def ignore_below(self, ignore_below=0):
        """Discards peaks whose intensity is below ``ignore_below``.

        After discarding peaks, the pattern will be renormalized to
        sum to ``1.0``

        Parameters
        ----------
        ignore_below : float, optional
            The threshold below which peaks will be discarded

        Returns
        -------
        TheoreticalIsotopicPattern
            self
        """
        total = 0
        kept_tid = []
        n = len(self)
        for i in range(n):
            p = self.get(i)
            if (p.intensity < ignore_below) and (i > 1):
                continue
            else:
                total += p.intensity
                p = p.clone()
                kept_tid.append(p)
        self.peaklist = kept_tid
        self.offest = self.origin - self.peaklist[0].mz
        n = len(self)
        for i in range(n):
            p = self.get(i)
            p.intensity /= total
        return self

    @property
    def monoisotopic_mz(self):
        return self.origin

    def __repr__(self):
        return "TheoreticalIsotopicPattern(%0.4f, charge=%d, (%s))" % (
            self.monoisotopic_mz,
            self.peaklist[0].charge,
            ', '.join("%0.3f" % p.intensity for p in self.peaklist))

    def scale(self, experimental_distribution, method='sum'):
        r"""Scales ``self``'s intensity to match the intensity distribution of the
        experimental isotopic pattern in ``experimental_distribution``.

        The ``method`` argument must be one of:

        "sum"
            Scale each peak of the theoretical distribution by the sum of the
            intensity in the experimental distribution such that the sums of their
            intensities are equal.

        "max"
            Select the most abundant peak in the theoretical distribution :math:`t_i`, find it's
            match in the experimental distribution :math:`e_i`, find the scaling factor
            :math:`\alpha = \frac{e_i}{t_i}` which will make :math:`e_i == t_i` and scale all
            peaks in self by :math:`alpha`

        Parameters
        ----------
        experimental_distribution : list
            The experimental peaks matched
        method : str, optional
            The scaling method to use. Defaults to ``"sum"``

        Returns
        -------
        TheoreticalIsotopicPattern
            self
        """
        if method == 'sum':
            total_abundance = sum(
                p.intensity for p in experimental_distribution)
            for peak in self:
                peak.intensity *= total_abundance
        elif method == 'max':
            i, peak = max(enumerate(self),
                          key=lambda x: x[1].intensity)
            scale_factor = experimental_distribution[
                i].intensity / peak.intensity
            for peak in self:
                peak.intensity *= scale_factor
        elif method == "meanscale":
            scales = 0
            weights = 0
            total = 0
            for i in range(len(experimental_distribution)):
                epeak = experimental_distribution[i]
                total += epeak.intensity
                tpeak = self[i]
                w = ((tpeak.intensity) * epeak.intensity ** 2)
                weights += w
                scales += (epeak.intensity / tpeak.intensity) * w

            scale_factor = scales / weights
            for peak in self:
                peak.intensity *= scale_factor

        return self

    def scale_raw(self, scale_factor):
        for peak in self:
            peak.intensity *= scale_factor
        return self

    def drop_last_peak(self):
        tail = self[-1]
        scaler = 1 - tail.intensity
        for p in self[:-1]:
            p.intensity /= scaler
        return scaler

    def total(self):
        return sum(p.intensity for p in self)

    def normalize(self):
        total = self.total()
        for peak in self:
            peak.intensity /= total
        return self


@dict_proxy("base_composition")
class Averagine(object):
    """An isotopic model which can be used to interpolate the composition
    of a class of molecule given an average monomer composition and a theoretical
    polymer mass

    Implements the :class:`Mapping` interface.

    Attributes
    ----------
    base_composition: Mapping
        A mapping from element symbol to average count (float) of that element
        for the average monomer
    base_mass : float
        The base mass of the average monomer. Calculated from :attr:`base_composition`
    """

    def __init__(self, base_composition):
        self.base_composition = dict(base_composition)
        self.base_mass = calculate_mass(self.base_composition)

    def scale(self, mz, charge=1, charge_carrier=PROTON):
        """Given an m/z and a charge state, interpolate the composition
        of the polymer with the matching neutral mass

        Parameters
        ----------
        mz : float
            The reference m/z to calculate the neutral mass to interpolate from
        charge : int, optional
            The reference charge state to calculate the neutral mass. Defaults to 1
        charge_carrier : float, optional
            The mass of the charge carrier. Defaults to the mass of a proton.

        Returns
        -------
        Mapping
            The interpolated composition for the calculated neutral mass,
            rounded to the nearest integer and hydrogen corrected.

        References
        ----------
        Senko, M. W., Beu, S. C., & McLafferty, F. W. (1995). Determination of monoisotopic masses and ion populations
        for large biomolecules from resolved isotopic distributions. Journal of the American Society for Mass
        Spectrometry, 6(4), 229–233. http://doi.org/10.1016/1044-0305(95)00017-8
        """
        neutral = neutral_mass(mz, charge, charge_carrier)

        scale = neutral / self.base_mass
        scaled = {}
        for elem, count in self.base_composition.items():
            scaled[elem] = round(count * scale)

        scaled_mass = calculate_mass(scaled)
        delta_hydrogen = round(scaled_mass - neutral)
        H = scaled["H"]
        if H > delta_hydrogen:
            scaled["H"] = H - delta_hydrogen
        else:
            scaled["H"] = 0

        return scaled

    def isotopic_cluster(self, mz, charge=1, charge_carrier=PROTON, truncate_after=0.95, ignore_below=0.0):
        """Generate a theoretical isotopic pattern for the given m/z and charge state, thresholded
        by theoretical peak height and density.

        Parameters
        ----------
        mz : float
            The reference m/z to calculate the neutral mass to interpolate from
        charge : int, optional
            The reference charge state to calculate the neutral mass. Defaults to 1
        charge_carrier : float, optional
            The mass of the charge carrier. Defaults to the mass of a proton.
        truncate_after : float, optional
            The percentage of the signal in the theoretical isotopic pattern to include.
            Defaults to 0.95, including the first 95% of the signal in the generated pattern
        ignore_below : float, optional
            Omit theoretical peaks whose intensity is below this number.
            Defaults to 0.0

        Returns
        -------
        :class:`.TheoreticalIsotopicPattern`
            The generated and thresholded pattern
        """
        composition = self.scale(mz, charge, charge_carrier)
        peaklist = isotopic_variants(composition, charge=charge)
        tid = TheoreticalIsotopicPattern(peaklist, peaklist[0].mz, 0)
        tid.shift(mz)
        if truncate_after < 1.0:
            tid.truncate_after(truncate_after)
        if ignore_below > 0:
            tid.ignore_below(ignore_below)
        return tid

    def __repr__(self):
        return "Averagine(%r)" % self.base_composition

    def __eq__(self, other):
        return self.base_composition == other.base_composition

    def __hash__(self):
        return hash(frozenset(self.base_composition.items()))


def average_compositions(compositions, weights=None):
    """Calculate the average composition

    Parameters
    ----------
    compositions: Iterable
        An Iterable of Mappings representing chemical compositions
    weights: Iterable, optional
        An optional weight vector

    Returns
    -------
    dict
        The average composition
    """
    n = 0
    if weights is None:
        weights = [1] * len(compositions)
    else:
        if len(weights) != len(compositions):
            raise ValueError("The size of weights must match the size of compositions")
    result = defaultdict(float)
    for i, comp in enumerate(compositions):
        w = weights[i]
        n += w
        for k, v in comp.items():
            result[k] += v * w
    for k, v in list(result.items()):
        result[k] = v / n
    return dict(result)


def add_compositions(a, b):
    a = defaultdict(float, **a)
    for k, v in b.items():
        a[k] += v
    return dict(a)


try:
    _Averagine = Averagine
    _TheoreticalIsotopicPattern = TheoreticalIsotopicPattern
    from ms_deisotope._c.averagine import Averagine, TheoreticalIsotopicPattern
except ImportError as e:
    print(e, "averagine")


peptide = Averagine({"C": 4.9384, "H": 7.7583, "N": 1.3577, "O": 1.4773, "S": 0.0417})
glycopeptide = Averagine({"C": 10.93, "H": 15.75, "N": 1.6577, "O": 6.4773, "S": 0.02054})
glycan = Averagine({'C': 7.0, 'H': 11.8333, 'N': 0.5, 'O': 5.16666})
permethylated_glycan = Averagine({'C': 12.0, 'H': 21.8333, 'N': 0.5, 'O': 5.16666})
heparin = Averagine({'H': 10.5, 'C': 6, 'S': 0.5, 'O': 5.5, 'N': 0.5})
heparan_sulfate = Averagine({'H': 10.667, 'C': 6.0, 'S': 1.333, 'O': 9.0, 'N': 0.667})


_neutron_shift = calculate_mass({"C[13]": 1}) - calculate_mass({"C[12]": 1})


def isotopic_shift(charge=1):
    return _neutron_shift / float(charge)


@dict_proxy("averagine")
class AveragineCache(object):
    """A wrapper around a :class:`Averagine` instance which will cache isotopic patterns
    produced for new (m/z, charge) pairs and reuses it for nearby m/z values

    Attributes
    ----------
    averagine : :class:`~Averagine`
        The averagine to use to generate new isotopic patterns
    cache_truncation : float
        Number of decimal places to round off the m/z for caching purposes
    """

    def __init__(self, averagine, backend=None, cache_truncation=1.0):
        if backend is None:
            backend = {}
        self.backend = backend
        self.averagine = Averagine(averagine)
        self.cache_truncation = cache_truncation

    def has_mz_charge_pair(self, mz, charge=1, charge_carrier=PROTON, truncate_after=0.95, ignore_below=0.0):
        if self.cache_truncation == 0.0:
            key_mz = mz
        else:
            key_mz = round(mz / self.cache_truncation) * self.cache_truncation
        if (key_mz, charge, charge_carrier) in self.backend:
            return self.backend[key_mz, charge, charge_carrier].clone().shift(mz)
        else:
            tid = self.averagine.isotopic_cluster(
                mz, charge, charge_carrier, truncate_after, ignore_below)
            self.backend[key_mz, charge, charge_carrier] = tid.clone()
            return tid

    def isotopic_cluster(self, mz, charge=1, charge_carrier=PROTON, truncate_after=0.95, ignore_below=0.0):
        """Generate a theoretical isotopic pattern for the given m/z and charge state, thresholded
        by theoretical peak height and density.

        Mimics :meth:`.Averagine.isotopic_cluster` but uses the object's cache through
        :meth:`has_mz_charge_pair`.

        Parameters
        ----------
        mz : float
            The reference m/z to calculate the neutral mass to interpolate from
        charge : int, optional
            The reference charge state to calculate the neutral mass. Defaults to 1
        charge_carrier : float, optional
            The mass of the charge carrier. Defaults to the mass of a proton.
        truncate_after : float, optional
            The percentage of the signal in the theoretical isotopic pattern to include.
            Defaults to 0.95, including the first 95% of the signal in the generated pattern
        ignore_below : float, optional
            Omit theoretical peaks whose intensity is below this number.
            Defaults to 0.0

        Returns
        -------
        :class:`.TheoreticalIsotopicPattern`
            The generated and thresholded pattern
        """
        return self.has_mz_charge_pair(mz, charge, charge_carrier, truncate_after, ignore_below)

    def __repr__(self):
        return "AveragineCache(%r)" % self.averagine

    def clear(self):
        self.backend.clear()


try:
    _AveragineCache = AveragineCache
    _isotopic_shift = isotopic_shift
    from ms_deisotope._c.averagine import AveragineCache, isotopic_shift
except ImportError:
    pass
