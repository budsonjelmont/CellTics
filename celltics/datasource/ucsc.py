from .datasource import DataSource
from urllib.request import urlopen
from urllib.error import URLError
from xml.parsers.expat import ExpatError
import xmltodict

# Define UCSC specific objects and data source class

class UCSC(DataSource):
  
  def __init__(self, baseurl, assembly, chr_aliases=None):
    self.baseurl = baseurl # http://genome.ucsc.edu 
    self.assembly =  assembly
    self.chr_aliases = chr_aliases
  
  def get_chrom_alias(self, chrom):
    return chrom

  def get_reference_seq(self, chrom, start, end):
      """
      UCSC http request to return reference sequence
      :param chrom:
      :param start:
      :param end:
      :return: dna reference sequence
      """
      if chrom.startswith('chr'):
          chrom = chrom.replace('chr', '')
      request = '{}/cgi-bin/das/{}/dna?segment=chr{}:{},{}'.format(self.baseurl, self.assembly, chrom, start, end)
      try:
          dna = xmltodict.parse(urlopen(request).read())['DASDNA']['SEQUENCE']['DNA']['#text'].replace('\n', '')
      except (URLError, ExpatError) as e:
          print('Could not open UCSC url.  Please check your internet connection.\n{}\n{}'.format(request, str(e)))
          dna = "n" * (start - end)
      return dna

