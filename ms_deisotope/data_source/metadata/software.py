from .cv import Term, render_list


def __generate_list_code():
    '''Prints the code to generate these static lists
    '''
    render_list('software', list_name='software_names',
                term_cls_name="SoftwareName")


class SoftwareName(Term):
    pass


class Software(object):

    @classmethod
    def is_name(cls, name):
        try:
            software_names_by_name[name]
            return True
        except KeyError:
            return False

    def __init__(self, name=None, id=None, version=None, **options):
        if name is None:
            name, options = self._resolve_name_from_kwargs(options)
        if name is None and id is not None:
            name = id
        self.name = name
        self.id = id or name
        self.version = version
        self.options = options

    def _resolve_name_from_kwargs(self, options):
        names = dict()
        not_names = dict()
        for key, value in options.items():
            if self.is_name(key):
                names[key] = value
            else:
                not_names[key] = value
        options = not_names
        if len(names) == 1:
            name = list(names.keys())[0]
        elif len(names) == 0:
            name = None
        else:
            raise ValueError("Multiple possible names found")
        return name, options

    def __str__(self):
        return self.name

    def __repr__(self):
        template = '{self.__class__.__name__}({self.name}, {self.id}, {self.version})'
        return template.format(self=self)

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return str(self) == str(other)


software_names = [
    SoftwareName(u'SCiLS software', u'MS:1002383',
                 u'SCiLS software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'acquisition software', u'MS:1001455',
                 u'Acquisition software.', 'software', [u'software']),
    SoftwareName(u'data processing software', u'MS:1001457',
                 u'Data processing software.', 'software', [u'software']),
    SoftwareName(u'analysis software', u'MS:1001456',
                 u'Analysis software.', 'software', [u'software']),
    SoftwareName(u'SCIEX software', u'MS:1000690',
                 u'SCIEX or Applied Biosystems software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'Applied Biosystems software', u'MS:1000691',
                 u'Applied Biosystems|MDS SCIEX software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'Bruker software', u'MS:1000692',
                 u'Bruker software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'Thermo Finnigan software', u'MS:1000693',
                 u'Thermo Finnigan software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'Waters software', u'MS:1000694',
                 u'Waters software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'SRM software', u'MS:1000871',
                 u'Software used to predict, select, or optimize transitions or analyze the results of selected reaction monitoring runs.', 'software', [u'software']),
    SoftwareName(u'peptide attribute calculation software', u'MS:1000873',
                 u'Software used to predict or calculate numerical attributes of peptides.', 'software', [u'software']),
    SoftwareName(u'Agilent software', u'MS:1000689',
                 u'Agilent software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'quantitation software name', u'MS:1001139', u'Quantitation software name.',
                 'software', [u'software', u'quantification information']),
    SoftwareName(u'LECO software', u'MS:1001798',
                 u'LECO software for data acquisition and analysis.', 'software', [u'software']),
    SoftwareName(u'custom unreleased software tool', u'MS:1000799',
                 u'A software tool that has not yet been released. The value should describe the software. Please do not use this term for publicly available software - contact the PSI-MS working group in order to have another CV term added.', 'software', [u'software']),
    SoftwareName(u'BSI software', u'MS:1001949',
                 u'Bioinformatics Solutions Inc. Software for data processing and analysis.', 'software', [u'software']),
    SoftwareName(u'Shimadzu Corporation software', u'MS:1001557',
                 u'Shimadzu Corporation software.', 'software', [u'software']),
    SoftwareName(u'SCiLS Lab', u'MS:1002384', u'SCiLS Lab software.', 'software', [
                 u'SCiLS software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Analyst', u'MS:1000551', u'SCIEX or Applied Biosystems|MDS SCIEX software for data acquisition.', 'software', [
                 u'SCIEX software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'apexControl', u'MS:1000706', u'Bruker software for data acquisition.',
                 'software', [u'Bruker software', u'acquisition software', u'software']),
    SoftwareName(u'MALDI Solutions LC-MALDI', u'MS:1002381', u'Software for automated LC-MALDI analysis and reporting.', 'software',
                 [u'acquisition software', u'analysis software', u'data processing software', u'Shimadzu Corporation software', u'software']),
    SoftwareName(u'dpControl', u'MS:1000720', u'Bruker software for data acquisition.',
                 'software', [u'Bruker software', u'acquisition software', u'software']),
    SoftwareName(u'esquireControl', u'MS:1000721', u'Bruker software for data acquisition.',
                 'software', [u'Bruker software', u'acquisition software', u'software']),
    SoftwareName(u'HCTcontrol', u'MS:1000725', u'Bruker software for data acquisition.',
                 'software', [u'Bruker software', u'acquisition software', u'software']),
    SoftwareName(u'micrOTOFcontrol', u'MS:1000726', u'Bruker software for data acquisition.',
                 'software', [u'Bruker software', u'acquisition software', u'software']),
    SoftwareName(u'spControl', u'MS:1000737', u'Bruker software for data acquisition.',
                 'software', [u'Bruker software', u'acquisition software', u'software']),
    SoftwareName(u'ChromaTOF HRT software', u'MS:1001877', u'Software for acquisition, processing and analysis of data for LECO instruments.',
                 'software', [u'acquisition software', u'analysis software', u'data processing software', u'LECO software', u'software']),
    SoftwareName(u'MALDI Solutions Microbial Identification', u'MS:1001878', u'Shimadzu Biotech software for data acquisition, processing, and analysis.', 'software', [
                 u'acquisition software', u'analysis software', u'data processing software', u'MALDI Solutions', u'software', u'Shimadzu Corporation software']),
    SoftwareName(u'6300 Series Ion Trap Data Analysis Software', u'MS:1000688', u'Software for data analysis of 6300 series ion trap mass spectrometers.',
                 'software', [u'Agilent software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ChromaTOF software', u'MS:1001799', u'Software for acquisition, processing and analysis of data for LECO instruments.',
                 'software', [u'acquisition software', u'analysis software', u'data processing software', u'LECO software', u'software']),
    SoftwareName(u'MassHunter Data Acquisition', u'MS:1000678', u'Software for data acquisition of 6000 series instruments.',
                 'software', [u'Agilent software', u'acquisition software', u'software']),
    SoftwareName(u'MassHunter Easy Access', u'MS:1000679', u'Software for open access data acquisition.',
                 'software', [u'Agilent software', u'acquisition software', u'software']),
    SoftwareName(u'GPS Explorer', u'MS:1000661', u'SCIEX or Applied Biosystems software for data acquisition and analysis.', 'software', [
                 u'SCIEX software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Voyager Biospectrometry Workstation System', u'MS:1000539', u'Applied Biosystems MALDI-TOF data acquisition and analysis system.',
                 'software', [u'Applied Biosystems software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Xcalibur', u'MS:1000532', u'Thermo Finnigan software for data acquisition and analysis.', 'software', [
                 u'Thermo Finnigan software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MassLynx', u'MS:1000534', u'Micromass software for data acquisition and analysis.', 'software', [
                 u'Waters software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'4700 Explorer', u'MS:1000537', u'Applied Biosystems software for data acquisition and analysis.', 'software', [
                 u'Applied Biosystems software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Data Explorer', u'MS:1000536', u'Applied Biosystems software for data acquisition and analysis.', 'software', [
                 u'Applied Biosystems software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'4000 Series Explorer Software', u'MS:1000659', u'SCIEX or Applied Biosystems software for data acquisition and analysis.',
                 'software', [u'SCIEX software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'FlexControl', u'MS:1000540', u'Bruker software for data acquisition.',
                 'software', [u'Bruker software', u'acquisition software', u'software']),
    SoftwareName(u'SCIEX TOF/TOF Series Explorer Software', u'MS:1001483', u'SCIEX or Applied Biosystems software for TOF/TOF data acquisition and analysis.',
                 'software', [u'SCIEX software', u'acquisition software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MALDI Solutions', u'MS:1001558', u'Shimadzu Biotech software for data acquisition, processing, and analysis.', 'software', [
                 u'acquisition software', u'analysis software', u'data processing software', u'Shimadzu Corporation software', u'software']),
    SoftwareName(u'Trapper', u'MS:1000553', u'A software program for converting Agilent MassHunter format to mzXML or mzML. Trapper was originally developed at the Institute for Systems Biology.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'CLINPROT', u'MS:1000708', u'Bruker CLINPROT software.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'CLINPROT micro', u'MS:1000709', u'Bruker CLINPROT micro software.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'BioTools', u'MS:1000707', u'Bruker software for data analysis.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'preprocessing software', u'MS:1002386', u'Preprocessing software.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'PIA', u'MS:1002387', u'PIA - Protein Inference Algorithms, a toolbox for protein inference and identification analysis." [PSI:PI', 'software', [
                 u'postprocessing software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'PEAKS Online', u'MS:1001947', u'PEAKS Online software for high throughput data analysis.', 'software', [
                 u'quantitation software name', u'analysis software', u'data processing software', u'software', u'quantification information']),
    SoftwareName(u'PEAKS Studio', u'MS:1001946', u'PEAKS Studio software for data analysis.', 'software', [
                 u'quantitation software name', u'analysis software', u'data processing software', u'software', u'quantification information']),
    SoftwareName(u'DataAnalysis', u'MS:1000719', u'Bruker software for data analysis.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'CompassXtract', u'MS:1000718', u'Bruker software library for data access.',
                 'software', [u'Bruker software', u'data processing software', u'software']),
    SoftwareName(u'Compass OpenAccess', u'MS:1000715', u'Bruker compass OpenAccess software.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Compass for micrOTOF', u'MS:1000714', u'Bruker Compass for micrOTOF software.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'CompassXport', u'MS:1000717', u'Bruker stand-alone software for data conversion.',
                 'software', [u'Bruker software', u'data processing software', u'software']),
    SoftwareName(u'Compass for HCT/esquire', u'MS:1000713', u'Bruker Compass for HCT/esquire software.',
                 'software', [u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Compass', u'MS:1000712', u'Bruker Compass software.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'flexImaging', u'MS:1000722', u'Bruker software for data analysis.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProfileAnalysis', u'MS:1000728', u'Bruker software for data analysis.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MSDK', u'MS:1002645', u'Mass Spectrometry Development Kit (MSDK) is a Java library of algorithms for processing of mass spectrometry data." [PSI:PI', 'software', [
                 u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'QuantAnalysis', u'MS:1000736', u'Bruker software for data analysis.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MzWiff', u'MS:1000591', u'A software program for converting Applied Biosystems wiff file format to the mzXML or mzML format. MzWiff is currently maintained at the Institute for Systems Biology. It replaces the slower mzStar program.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'SQID', u'MS:1001886', u'Software for data analysis of peptides and proteins.',
                 'software', [u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Maltcms', u'MS:1002344', u'Modular Application Toolkit for Chromatography Mass-Spectrometry is an application framework mainly for developers." [PSI:PI', 'software', [
                 u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MZmine', u'MS:1002342', u'A framework for differential analysis of mass spectrometry data." [PMID:16403790', 'software', [
                 u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'PepFinder', u'MS:1002524', u'Thermo Scientific PepFinder BioPharma analysis software.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'Spectrum Mill for MassHunter Workstation', u'MS:1000687', u'Software for protein identification and characterization of complex protein digest mixtures.',
                 'software', [u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'METLIN', u'MS:1000686', u'Personal Metabolite Database for MassHunter Workstation. Software for identification of human metabolites.',
                 'software', [u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MassHunter Mass Profiler', u'MS:1000685', u'Software for quantitation and statistical analysis of TOF and Q-TOF LC/MS data.',
                 'software', [u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Genespring MS', u'MS:1000684', u'Software for quantitation and statistical analysis of TOF and Q-TOF LC/MS data.',
                 'software', [u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MassHunter BioConfirm', u'MS:1000683', u'Software for protein characterization.', 'software', [
                 u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MassHunter Metabolite ID', u'MS:1000682', u'Software for identification of metabolites.', 'software', [
                 u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MassHunter Quantitative Analysis', u'MS:1000681', u'Software for quantitation of Triple Quadrupole and Quadrupole Time-of-Flight data.',
                 'software', [u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MassHunter Qualitative Analysis', u'MS:1000680', u'Software for data analysis of data from 6000 series instruments.',
                 'software', [u'Agilent software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'postprocessing software', u'MS:1002414', u'Postprocessing software.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'XCMS', u'MS:1001582', u'Bioconductor package XCMS for preprocessing high-throughput, untargeted analyte profiling data.',
                 'software', [u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'UNIFY', u'MS:1001796', u'Waters UNIFY software for liquid chromatography and mass spectrometry acquisition.',
                 'software', [u'Waters software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Empower', u'MS:1001795', u'Waters Empower software for liquid chromatography and mass spectrometry acquisition.',
                 'software', [u'Waters software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Pro Quant', u'MS:1000670', u'Applied Biosystems|MDS SCIEX software for protein ID and quant by iTRAQ.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Pro BLAST', u'MS:1000671', u'Applied Biosystems|MDS SCIEX software for MS-BLAST identification.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MultiQuant', u'MS:1000674', u'Applied Biosystems|MDS SCIEX software for MRM-based quantitation.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteinPilot Software', u'MS:1000663', u'SCIEX or Applied Biosystems|MDS SCIEX software for protein ID and quant.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'LightSight Software', u'MS:1000662', u'SCIEX or Applied Biosystems|MDS SCIEX software metabolite identification.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MarkerView Software', u'MS:1000665', u'Applied Biosystems|MDS SCIEX software for metabolomics and biomarker profiling.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TissueView Software', u'MS:1000664', u'Applied Biosystems|MDS SCIEX software for tissue imaging.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'BioAnalyst', u'MS:1000667', u'Applied Biosystems|MDS SCIEX software for bio-related data exploration.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MRMPilot Software', u'MS:1000666', u'Applied Biosystems|MDS SCIEX software for MRM assay development.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Pro ICAT', u'MS:1000669', u'Applied Biosystems|MDS SCIEX software for protein ID and quant by ICAT.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Pro ID', u'MS:1000668', u'Applied Biosystems|MDS SCIEX software for protein identification.',
                 'software', [u'SCIEX software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'PRIDE Converter2', u'MS:1002335', u'Java software designed to convert one of several proteomics identification results formats into PRIDE XML.',
                 'software', [u'conversion software', u'data processing software', u'software']),
    SoftwareName(u'ProCon', u'MS:1002334', u'Java software designed to convert one of several proteomics identification results formats into mzIdentML or PRIDE XML." [PSI:PI', 'software', [
                 u'conversion software', u'data processing software', u'software']),
    SoftwareName(u'conversion software', u'MS:1002333', u'Computer software primarily designed to convert data represented in one format to another format, sometimes with minor data alterations in the process.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'PEAKS Node', u'MS:1001948', u'PEAKS Node software for high throughput data analysis.', 'software', [
                 u'quantitation software name', u'analysis software', u'data processing software', u'software', u'quantification information']),
    SoftwareName(u'massWolf', u'MS:1000538', u'A software for converting Waters raw directory format to mzXML or mzML. MassWolf was originally developed at the Institute for Systems Biology.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'Bioworks', u'MS:1000533', u'Thermo Finnigan software for data analysis of peptides and proteins.',
                 'software', [u'Thermo Finnigan software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'FlexAnalysis', u'MS:1000535', u'Bruker software for data analysis.', 'software', [
                 u'Bruker software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Proteome Discoverer', u'MS:1000650', u'Thermo Scientific software for data analysis of peptides and proteins.',
                 'software', [u'Thermo Finnigan software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MSnbase', u'MS:1002870', u'Bioconductor package MSnbase provides infrastructure for manipulation, processing and visualization of mass spectrometry and proteomics data, ranging from raw to quantitative and annotated data.',
                 'software', [u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'CAMERA', u'MS:1002871', u'Bioconductor package CAMERA for annotation of peak lists generated by xcms, rule based annotation of isotopes and adducts, isotope validation, EIC correlation based tagging of unknown adducts and fragments.',
                 'software', [u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'mzR', u'MS:1002869', u'Bioconductor package mzR for reading and writing mass spectrometry data files.',
                 'software', [u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'pymzML', u'MS:1001914', u'Python module to interface mzML Data.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'ReAdW', u'MS:1000541', u'A software program for converting Thermo Finnigan RAW file format to mzXML or mzML. ReAdW was originally developed at the Institute for Systems Biology. Its whimsical interleaved spelling and capitalization is pronounced \\"readraw\\".',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'MzStar', u'MS:1000542', u'A software program for converting Applied Biosystems wiff file format to mzXML format. MzStar was originally developed at the Institute for Systems Biology. It is now obsoleted by the MzWiff program.',
                 'software', [u'data processing software', u'software']),
    SoftwareName(u'Maui', u'MS:1002452', u'The Maltcms Graphical User Interface." [PSI:PI', 'software', [
                 u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP software', u'MS:1000752', u'TOPP (The OpenMS proteomics pipeline) software.',
                 'software', [u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteoWizard software', u'MS:1000615', u'ProteoWizard software for data processing and analysis. Primarily developed by the labs of P. Malick and D. Tabb.',
                 'software', [u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'PinPoint', u'MS:1001912', u'Thermo Scientific PinPoint SRM analysis software.', 'software', [
                 u'Thermo Finnigan software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteinLynx Global Server', u'MS:1000601', u'Waters software for data analysis.', 'software', [
                 u'Waters software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Proteios', u'MS:1000600', u'Database application and analysis platform for proteomics." [PSI:MS', 'software', [
                 u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Tide', u'MS:1002575', u'Tide open-source sequence search program developed at the University of Washington.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Morpheus', u'MS:1002661', u'Morpheus search engine.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Mascot Distiller', u'MS:1001488', u'Mascot Distiller.', 'software', [
                 u'quantitation software name', u'analysis software', u'software', u'quantification information']),
    SoftwareName(u'IsobariQ', u'MS:1002210', u'A quantitative software package designed for analysis of IPTL, TMT and iTRAQ data." [PMID:21067241, DOI:10.1021/pr1009977', 'software', [
                 u'quantitation software name', u'analysis software', u'software', u'quantification information']),
    SoftwareName(u'Ascore software', u'MS:1001984', u'Ascore software.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'ProteinScape', u'MS:1000734', u'Bruker ProteinScape software.',
                 'software', [u'Bruker software', u'analysis software', u'software']),
    SoftwareName(u'greylag', u'MS:1001461', u'Greylag identification software.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Mascot Parser', u'MS:1001478', u'Mascot Parser was used to analyze the spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'SpectraST', u'MS:1001477', u'SpectraST was used to analyze the spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'X\\!Tandem', u'MS:1001476', u'X!Tandem was used to analyze the spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'OMSSA', u'MS:1001475', u'Open Mass Spectrometry Search Algorithm was used to analyze the spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'mzidLib', u'MS:1002237', u'A library of Java routines for manipulating mzIdentML files.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Pepitome', u'MS:1001588', u'Tabb Lab software for spectral library searches on tandem mass spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'MaxQuant', u'MS:1001583', u'MaxQuant is a quantitative proteomics software package designed for analyzing large mass spectrometric data sets. It is specifically aimed at high resolution MS data.',
                 'software', [u'quantitation software name', u'analysis software', u'software', u'quantification information']),
    SoftwareName(u'Comet', u'MS:1002251', u'Comet open-source sequence search engine developed at the University of Washington.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Andromeda', u'MS:1002337', u'Andromeda is a peptide search engine.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Amanda', u'MS:1002336', u'Amanda scoring system for PSM identification.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'SEQUEST', u'MS:1001208', u'The name of the SEQUEST search engine.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Phenyx', u'MS:1001209', u'The name of the Phenyx search engine.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Mascot', u'MS:1001207', u'The name of the Mascot search engine.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Percolator', u'MS:1001490', u'Percolator.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'small molecule analysis software', u'MS:1002878',
                 u'Software for the analysis of small molecules.', 'software', [u'analysis software', u'software']),
    SoftwareName(u'ProteinExtractor', u'MS:1001487', u"An algorithm for protein determination/assembly integrated into Bruker's ProteinScape.",
                 'software', [u'Bruker software', u'analysis software', u'software']),
    SoftwareName(u'Mascot Integra', u'MS:1001489', u'Mascot Integra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Byonic', u'MS:1002261', u'Byonic search engine from Protein Metrics.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'PeptideShaker', u'MS:1002458', u'PeptideShaker is a software for the interpretation of proteomics identification results." [PSI:PI', 'software', [
                 u'analysis software', u'software']),
    SoftwareName(u'TagRecon', u'MS:1001587', u'Tabb Lab software for reconciling sequence tags to a protein database.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'DirecTag', u'MS:1001586', u'Tabb Lab software for generating sequence tags from tandem mass spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'MyriMatch', u'MS:1001585', u'Tabb Lab software for directly comparing peptides in a database to tandem mass spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'PAnalyzer', u'MS:1002076', u'PAnalyzer software for getting protein evidence categories.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'NIST MSPepSearch', u'MS:1002750', u'Search tool of the NIST (National Institute of Standards and Technology) for spectral library searches.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Trans-Proteomic Pipeline', u'MS:1002285',
                 u'A suite of open source tools for the processing of MS2 proteomics data developed by the Seattle Proteome Center at the Institute for Systems Biology.', 'software', [u'analysis software', u'software']),
    SoftwareName(u'Trans-Proteomic Pipeline software', u'MS:1002286',
                 u'A software program that is a component of the Trans-Proteomic Pipeline.', 'software', [u'analysis software', u'software']),
    SoftwareName(u'DTASelect', u'MS:1002598', u'Analysis software designed to reassemble the SEQUEST peptide identifications and to highlight the most significant matches." [PMID:12643522', 'software', [
                 u'analysis software', u'software']),
    SoftwareName(u'MSQuant', u'MS:1001977', u'MSQuant software.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'DeBunker', u'MS:1001973', u'DeBunker software.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Scaffold', u'MS:1001561', u'Scaffold analysis software.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'ProLuCID', u'MS:1002596', u'The SEQUEST-like sequence search engine ProLuCID, developed in the Yates Lab at the Scripps Research Institute.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'xiFDR', u'MS:1002543', u'Target/Decoy based FDR estimation for cross-linking peptide-identifications.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Skyline mzQuantML converter', u'MS:1002546', u'A software package to convert Skyline report to mzQuantML." [PSI:PI', 'software', [
                 u'quantitation software name', u'analysis software', u'software', u'quantification information']),
    SoftwareName(u'xi', u'MS:1002544', u'Search engine for cross-linked peptides.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'MSPathFinder', u'MS:1002720', u'PNNL top-down/bottom-up analysis software for identifying peptides and proteoforms in fragmentation mass spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'MetaMorpheus', u'MS:1002826', u'MetaMorpheus search engine.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'MS-GF', u'MS:1002047',
                 u'MS-GF software used to re-score the peptide-spectrum matches." [DOI:10.1074/mcp.M110.003731', 'software', [u'analysis software', u'software']),
    SoftwareName(u'ProteinProspector', u'MS:1002043', u'ProteinProspector software for data acquisition and analysis.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'MS-GF+', u'MS:1002048', u'MS-GF+ software used to analyze the spectra.',
                 'software', [u'analysis software', u'software']),
    SoftwareName(u'Cliquid', u'MS:1000672', u'SCIEX Cliquid software for data analysis and quantitation.',
                 'software', [u'SCIEX software', u'software']),
    SoftwareName(u'MIDAS Workflow Designer', u'MS:1000673',
                 u'Applied Biosystems|MDS SCIEX software for MRM assay development.', 'software', [u'SCIEX software', u'software']),
    SoftwareName(u'Compass Security Pack', u'MS:1000716',
                 u'Bruker compass Security Pack software.', 'software', [u'Bruker software', u'software']),
    SoftwareName(u'ClinProTools', u'MS:1000711', u'Bruker ClinProTools software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'CLINPROT robot', u'MS:1000710', u'Bruker CLINPROT robot software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'GENOLINK', u'MS:1000723', u'Bruker GENOLINK software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'GenoTools', u'MS:1000724', u'Bruker GenoTools software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'PolyTools', u'MS:1000727', u'Bruker PolyTools software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'PROTEINEER', u'MS:1000729', u'Bruker PROTEINEER software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'PureDisk', u'MS:1000735', u'BrukerPureDisk software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'PROTEINEER-LC', u'MS:1000733', u'Bruker PROTEINEER-LC software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'PROTEINEER spII', u'MS:1000732', u'Bruker PROTEINEER spII software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'PROTEINEER fc', u'MS:1000731', u'Bruker PROTEINEER fc software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'PROTEINEER dp', u'MS:1000730', u'Bruker PROTEINEER dp software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'WARP-LC', u'MS:1000739', u'Bruker WARP-LC software.', 'software',
                 [u'Bruker software', u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'TargetAnalysis', u'MS:1000738', u'Bruker TargetAnalysis software.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'HyStar', u'MS:1000817', u'Bruker software for hyphenated experiments.',
                 'software', [u'Bruker software', u'software']),
    SoftwareName(u'Anubis', u'MS:1002410', u'Anubis software for selected reaction monitoring data." [PSI:PI', 'software', [
                 u'SRM software', u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'ATAQS', u'MS:1000925', u'Software suite used to predict, select, and optimize transitions as well as analyze the results of selected reaction monitoring runs developed and distributed by the Institute for Systems Biology.',
                 'software', [u'SRM software', u'software']),
    SoftwareName(u'Skyline', u'MS:1000922', u'Software used to predict, select, and optimize transitions as well as analyze the results of selected reaction monitoring runs developed and distributed by the MacCoss lab at the University of Washington." [https://brendanx-uw1.gs.washington.edu/labkey/wiki/home/software/Skyline/page.view?name=defaul', 'software', [
                 u'SRM software', u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'TIQAM', u'MS:1000923', u'Software used to predict, select, and optimize transitions for selected reaction monitoring experiments developed and distributed by the Institute for Systems Biology.',
                 'software', [u'SRM software', u'software']),
    SoftwareName(u'MaRiMba', u'MS:1000872', u'Software used to predict transitions for selected reaction monitoring experiments based on observed spectrum libraries developed and distributed by the Institute for Systems Biology.',
                 'software', [u'SRM software', u'software']),
    SoftwareName(u'MRMaid', u'MS:1002220', u"A web-based SRM assay design tool whose transitions are generated by mining the millions of identified peptide spectra held in the EBI's PRIDE database.",
                 'software', [u'SRM software', u'software']),
    SoftwareName(u'SSRCalc', u'MS:1000874', u'Sequence Specific Retention Calculator estimates the retention time of peptides based on their sequence.',
                 'software', [u'peptide attribute calculation software', u'software']),
    SoftwareName(u'SILACAnalyzer', u'MS:1001831', u'Software for SILAC workflow.', 'software', [
                 u'quantitation software name', u'TOPP software', u'software', u'quantification information', u'analysis software', u'data processing software']),
    SoftwareName(u'Progenesis LC-MS', u'MS:1001830', u'Software from Nonlinear Dynamics for LC-MS label-free workflow.',
                 'software', [u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'FindPairs', u'MS:1002063', u'Software e.g. for SILAC and 14N/15N workflow, part of the PeakQuant suite.',
                 'software', [u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'Microsoft Excel', u'MS:1002059', u'Microsoft Excel (can be used for spectral counting).',
                 'software', [u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'ProteoSuite', u'MS:1002124', u'ProteoSuite software for the analysis of quantitative proteomics data." [DOI:10.1089/omi.2012.0022, PMID:22804616', 'software', [
                 u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'x-Tracker', u'MS:1002123', u'X-Tracker generic tool for quantitative proteomics.',
                 'software', [u'quantitation software name', u'software', u'quantification information']),
    SoftwareName(u'ITRAQAnalyzer', u'MS:1002129', u'Software for iTRAQ workflow. Extracts and normalizes iTRAQ information from an MS experiment.', 'software', [
                 u'quantitation software name', u'TOPP software', u'software', u'quantification information', u'analysis software', u'data processing software']),
    SoftwareName(u'TOPP noise filter', u'MS:1002131', u'Noise filter component of the TOPP software.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP spectra filter', u'MS:1002137', u'Spectra filter component of the TOPP software.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP peak picker', u'MS:1002134', u'Peak picker component of the TOPP software.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP map aligner', u'MS:1002147', u'Map aligner component of the TOPP software.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MassTraceExtractor', u'MS:1002159', u'Annotates mass traces in centroided LC/MS maps.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MzTabExporter', u'MS:1002158', u'Exports various XML formats to an mzTab file.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP IDMerger', u'MS:1002155', u'Merges several protein/peptide identification files into one file.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP DTAExtractor', u'MS:1002154', u'Extracts spectra of an MS run file to several files in DTA format.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraMerger', u'MS:1002157', u'Merges spectra from an LC/MS map, either by precursor or by RT blocks.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP IDFileConverter', u'MS:1002156', u'Converts identification engine file formats.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP PrecursorMassCorrector', u'MS:1002160', u'Correct the precursor entries of tandem MS scans.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP HighResPrecursorMassCorrector', u'MS:1002161', u'Performs precursor mz correction on centroided high resolution data.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP AdditiveSeries', u'MS:1002162', u'Computes an additive series to quantify a peptide in a set of samples.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP Decharger', u'MS:1002163', u'Decharges and merges different feature charge variants of the same chemical entity.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP EICExtractor', u'MS:1002164', u'Quantifies signals at given positions in (raw or picked) LC/MS maps.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP feature finder', u'MS:1002165', u'Feature finder component of the TOPP software.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP ConsensusID', u'MS:1002188', u'Computes a consensus identification from peptide identifications of several identification engines.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP IDConflictResolver', u'MS:1002189', u'Resolves ambiguous annotations of features with peptide identifications.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP software adaptor', u'MS:1002180', u'Software adaptor to an external program in the TOPP software.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpecLibSearcher', u'MS:1002187', u'Identifies peptide MS2 spectra by spectral matching with a searchable spectral library.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP feature linker', u'MS:1002174', u'Feature linker component of the TOPP software.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MapRTTransformer', u'MS:1002173', u'Applies retention time transformations to maps.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP ConsensusMapNormalizer', u'MS:1002172', u'Normalizes maps of one consensus XML file (after linking).',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP ProteinQuantifier', u'MS:1002171', u'Computes protein abundances from annotated feature/consensus maps.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP CompNovoCID', u'MS:1002179', u'Performs a peptide/protein identification with the CompNovo engine in collision-induced dissociation (CID) mode.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP CompNovo', u'MS:1002178', u'Performs a peptide/protein identification with the CompNovo engine.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP ProteinInference', u'MS:1002203', u'Infer proteins from a list of (high-confidence) peptides.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FalseDiscoveryRate', u'MS:1002204', u'Estimates the false discovery rate on peptide and protein level using decoy searches.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP IDMapper', u'MS:1002191', u'Assigns protein/peptide identifications to feature or consensus features.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP IDFilter', u'MS:1002190', u'Filters results from protein or peptide identification engines based on different criteria.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP IDRTCalibration', u'MS:1002193', u'Calibrate Retention times of peptide hits to standards.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP IDPosteriorErrorProbability', u'MS:1002192', u'Estimates posterior error probabilities using a mixture model.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP PrecursorIonSelector', u'MS:1002195', u'A tool for precursor ion selection based on identification results.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP PeptideIndexer', u'MS:1002194', u'Refreshes the protein references for all peptide hits.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP OpenSwath component', u'MS:1002197', u'OpenSwath component of the TOPP software.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MRMMapper', u'MS:1002196', u'MRMMapper maps measured chromatograms (mzML) and the transitions used (TraML).',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'OpenXQuest', u'MS:1002673', u'Cross-Linking MS search engine.', 'software',
                 [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'BaselineFilter', u'MS:1000753', u'Removes the baseline from profile spectra using a top-hat filter.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'DBImporter', u'MS:1000755', u'Imports data to an OpenMS database.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'DBExporter', u'MS:1000754', u'Exports data from an OpenMS database to a file.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'FileFilter', u'MS:1000757', u'Extracts or manipulates portions of data from peak, feature or consensus feature files.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'FileConverter', u'MS:1000756', u'Converts between different MS file formats.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'InternalCalibration', u'MS:1000759', u'Applies an internal calibration.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'FileMerger', u'MS:1000758', u'Merges several MS files into one file.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'Resampler', u'MS:1000764', u'Transforms an LC/MS map into a resampled map or a png image.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'SpectraFilter', u'MS:1000765', u'OBSOLETE Applies a filter to peak spectra.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOFCalibration', u'MS:1000766', u'Applies time of flight calibration.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MapAligner', u'MS:1000760', u'OBSOLETE Corrects retention time distortions between maps.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'MapNormalizer', u'MS:1000761', u'Normalizes peak intensities in an MS run.', 'software', [
                 u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'NoiseFilter', u'MS:1000762', u'OBSOLETE Removes noise from profile spectra by using different smoothing techniques.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'PeakPicker', u'MS:1000763', u'OBSOLETE Finds mass spectrometric peaks in profile mass spectra.',
                 'software', [u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteoWizard SeeMS', u'MS:1002209', u'An interactive GUI application to view and filter mass spectrometry data in a variety of formats.',
                 'software', [u'ProteoWizard software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteoWizard msaccess', u'MS:1002208', u'Filters, processes, and displays mass spectrometry data in a variety of ways.',
                 'software', [u'ProteoWizard software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteoWizard msconvert', u'MS:1002205', u'Converts, filters, and processes mass spectrometry data in variety of formats.',
                 'software', [u'ProteoWizard software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteoWizard chainsaw', u'MS:1002207', u'Filters and processes protein sequence databases.', 'software', [
                 u'ProteoWizard software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'ProteoWizard idconvert', u'MS:1002206', u'Converts, filters, and processes identifications from shotgun proteomics experiments.',
                 'software', [u'ProteoWizard software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'mzidLib:Omssa2Mzid', u'MS:1002238', u'A converter for OMSSA OMX to mzIdentML.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:Tandem2Mzid', u'MS:1002239', u'A converter for Tandem XML to mzIdentML.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:Csv2Mzid', u'MS:1002240', u'A converter for CSV files (following OMSSA CSV style) to mzIdentML.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:Mzidentml2Csv', u'MS:1002245', u'A tool for converting mzIdentML files to CSV format.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:FalseDiscoveryRate', u'MS:1002244', u'A routine for calculating local FDR, q-value and FDRScore for mzIdentML files, based on a decoy search.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:InsertMetaDataFromFasta', u'MS:1002247', u'A tool for adding additional meta data from a FASTA file to DBSequence entries (sequence and description) in mzIdentML files.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:CombineSearchEngines', u'MS:1002246', u'A tool for combining results analysed in parallel in two or three search engines into a single mzIdentML file.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:ProteoGrouper', u'MS:1002241', u'A generic and parameterizable protein inference algorithm for mzIdentML files.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:Perform emPAI on mzid', u'MS:1002243', u'A routine for adding emPAI quantitative values to an mzIdentML file.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'mzidLib:Thresholder', u'MS:1002242', u'A routine for keeping only identifications passing a given threshold or setting passThreshold to true or false for SpectrumIdentificationItem or ProteinDetectionHypothesis in mzIdentML files.',
                 'software', [u'mzidLib', u'analysis software', u'software']),
    SoftwareName(u'Progenesis QI', u'MS:1002879', u'Metabolomics analysis software for LC-MS data from Nonlinear Dynamics.',
                 'software', [u'small molecule analysis software', u'analysis software', u'software']),
    SoftwareName(u'MyCompoundID', u'MS:1002881', u'Metabolite identification tool MyCompoundID." [PSI:PI', 'software', [
                 u'small molecule analysis software', u'analysis software', u'software']),
    SoftwareName(u'Compound Discoverer', u'MS:1002880', u'Metabolomics analysis software from Thermo Fisher Scientific.',
                 'software', [u'small molecule analysis software', u'analysis software', u'software']),
    SoftwareName(u'ASAPRatio', u'MS:1002574', u'A program in the TPP that calculates PSM, peptide, and protein-level abundances based on 2-channel isotope-labelled data such as ICAT, SILAC, etc.',
                 'software', [u'Trans-Proteomic Pipeline software', u'analysis software', u'software']),
    SoftwareName(u'PTMProphet', u'MS:1002292', u'A program in the TPP that calculates PTM localization probabilities by re-analyzing the peaks that are available to distinguish between possible modification sites.',
                 'software', [u'Trans-Proteomic Pipeline software', u'analysis software', u'software']),
    SoftwareName(u'XPRESS', u'MS:1002290', u'A program in the TPP that calculates PSM-level abundances based on 2-channel isotope-labelled data such as ICAT, SILAC, etc.',
                 'software', [u'Trans-Proteomic Pipeline software', u'analysis software', u'software']),
    SoftwareName(u'Libra', u'MS:1002291', u'A program in the TPP that calculates PSM, peptide, and protein-level abundances based on N-channel isobaric label peptide data such as iTRAQ, TMT, etc.',
                 'software', [u'Trans-Proteomic Pipeline software', u'analysis software', u'software']),
    SoftwareName(u'PeptideProphet', u'MS:1002287', u'A program in the TPP that calculates PSM probabilities for MS2 proteomics data searched with any of the supported sequence or spectral library search engines via the pepXML format." [PMID:12403597', 'software', [
                 u'Trans-Proteomic Pipeline software', u'analysis software', u'software']),
    SoftwareName(u'ProteinProphet', u'MS:1002289', u'A program in the TPP that calculates protein-level probabilities based on input PSM or peptide-level probabilities from PeptideProphet or iProphet. The output is written in the protXML format.',
                 'software', [u'Trans-Proteomic Pipeline software', u'analysis software', u'software']),
    SoftwareName(u'iProphet', u'MS:1002288', u'A program in the TPP that calculates distinct peptide probabilities based on several lines of corroborating evidence including search results from multiple search engines via the pepXML format.',
                 'software', [u'Trans-Proteomic Pipeline software', u'analysis software', u'software']),
    SoftwareName(u'TOPP NoiseFilterSGolay', u'MS:1002133', u'Removes noise from profile spectra by using a Savitzky-Golay smoothing.',
                 'software', [u'TOPP noise filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP NoiseFilterGaussian', u'MS:1002132', u'Removes noise from profile spectra by using a gaussian smoothing.',
                 'software', [u'TOPP noise filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterMarkerMower', u'MS:1002139', u'Applies a filter to peak spectra for marked peaks.', 'software', [
                 u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterBernNorm', u'MS:1002138', u'Applies a Bern et al normalization to peak spectra." [PMID:15262780', 'software', [
                 u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterWindowMower', u'MS:1002146', u'Applies a filter of the largest peaks in a sliding window over a peak spectrum.',
                 'software', [u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterSqrtMower', u'MS:1002144', u'Applies a filter to peak spectra after intensity scaling to the square root.',
                 'software', [u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterThresholdMower', u'MS:1002145', u'Applies a filter of peaks below a given threshold to peak spectra.',
                 'software', [u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterParentPeakMower', u'MS:1002142', u'Filters putative unfragmented precursor ions from tandem spectra.',
                 'software', [u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterScaler', u'MS:1002143', u'Applies a filter to peak spectra after intensity scaling according to rank.',
                 'software', [u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterNLargest', u'MS:1002140', u'Retains the n largest peaks of a peak spectra.', 'software', [
                 u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP SpectraFilterNormalizer', u'MS:1002141', u'Applies a TIC/maximal intensity normalization to peak spectra.',
                 'software', [u'TOPP spectra filter', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP PeakPickerWavelet', u'MS:1002136', u'Finds mass spectrometric peaks with a wavelet algorithm in low-resoluted profile mass spectra.',
                 'software', [u'TOPP peak picker', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP PeakPickerHiRes', u'MS:1002135', u'Finds mass spectrometric peaks in high-resoluted profile mass spectra.',
                 'software', [u'TOPP peak picker', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MapAlignerIdentification', u'MS:1002148', u'Corrects retention time distortions between maps based on common peptide identifications.',
                 'software', [u'TOPP map aligner', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MapAlignerPoseClustering', u'MS:1002149', u'Corrects retention time distortions between maps using a pose clustering approach.',
                 'software', [u'TOPP map aligner', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MapAlignerSpectrum', u'MS:1002150', u'Corrects retention time distortions between maps by spectrum alignment.',
                 'software', [u'TOPP map aligner', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureFinderCentroided', u'MS:1002166', u'Detects two-dimensional features in centroided LC-MS data.',
                 'software', [u'TOPP feature finder', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureFinderRaw', u'MS:1002167', u'Detects two-dimensional features in uncentroided LC-MS data.',
                 'software', [u'TOPP feature finder', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureFinderIsotopeWavelet', u'MS:1002168', u'Detects two-dimensional features in uncentroided LC-MS data with a wavelet algorithm.',
                 'software', [u'TOPP feature finder', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureFinderMetabo', u'MS:1002169', u'Detects two-dimensional features in centroided LC-MS data of metabolites.',
                 'software', [u'TOPP feature finder', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureFinderMRM', u'MS:1002170', u'Quantifies features LC-MS/MS MRM data.', 'software',
                 [u'TOPP feature finder', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MascotAdapter', u'MS:1002182', u'Identifies MS2 spectra using the external program Mascot.', 'software', [
                 u'TOPP software adaptor', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP MascotAdapterOnline', u'MS:1002183', u'Identifies MS2 spectra using the online version of the external program Mascot.',
                 'software', [u'TOPP software adaptor', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP InspectAdapter', u'MS:1002181', u'Identifies MS2 spectra using the external program Inspect.', 'software', [
                 u'TOPP software adaptor', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP XTandemAdapter', u'MS:1002186', u'Identifies MS2 spectra using the external program XTandem.', 'software', [
                 u'TOPP software adaptor', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP OMSSAAdapter', u'MS:1002184', u'Identifies MS2 spectra using the external program OMSSA.', 'software', [
                 u'TOPP software adaptor', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP PepNovoAdapter', u'MS:1002185', u'Identifies MS2 spectra using the external program PepNovo.', 'software', [
                 u'TOPP software adaptor', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureLinkerUnlabeledQT', u'MS:1002177', u'Groups corresponding features from multiple maps using a quality threshold clustering approach.',
                 'software', [u'TOPP feature linker', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureLinkerUnlabeled', u'MS:1002176', u'Groups corresponding features from multiple maps.', 'software', [
                 u'TOPP feature linker', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP FeatureLinkerLabeled', u'MS:1002175', u'Groups corresponding isotope-labeled features in a feature map.',
                 'software', [u'TOPP feature linker', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP OpenSwathFeatureXMLToTSV', u'MS:1002201', u'Converts a featureXML to a mProphet tsv (tab separated values).', 'software', [
                 u'TOPP OpenSwath component', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP OpenSwathDecoyGenerator', u'MS:1002200', u'Generates decoys according to different models for a specific TraML.',
                 'software', [u'TOPP OpenSwath component', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP OpenSwathRTNormalizer', u'MS:1002202', u'Generates a transformation file for retention time space into normalized space.',
                 'software', [u'TOPP OpenSwath component', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP OpenSwathChromatogramExtractor', u'MS:1002199', u'Extract chromatograms (XIC) from a MS2 map file.', 'software', [
                 u'TOPP OpenSwath component', u'TOPP software', u'analysis software', u'data processing software', u'software']),
    SoftwareName(u'TOPP OpenSwathAnalyzer', u'MS:1002198', u'Picks peaks and finds features in an SRM experiment.', 'software', [
                 u'TOPP OpenSwath component', u'TOPP software', u'analysis software', u'data processing software', u'software']),
]


software_names_by_name = {c.name: c for c in software_names}


def software_name(name):
    try:
        return software_names_by_name[name]
    except KeyError:
        return SoftwareName(name, name, name, name, [name])


if __name__ == '__main__':
    __generate_list_code()
