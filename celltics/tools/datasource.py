from urllib.request import urlopen
from urllib.error import URLError
from xml.parsers.expat import ExpatError
import xmltodict

class DataSource:
  def __init__(self, baseurl, assembly, chr_aliases):
    self.baseurl = baseurl 
    self.assembly =  assembly
    self.chr_aliases = chr_aliases

  def get_chrom_alias():
    pass

  def get_reference_seq():
    pass


# Define SeqRepo specific objects and data source class

seqrepo_aliases = {'grch37':{
  '1':'NC_000001.10',
  '2':'NC_000002.11',
  '3':'NC_000003.11',
  '4':'NC_000004.11',
  '5':'NC_000005.9',
  '6':'NC_000006.11',
  '7':'NC_000007.13',
  '8':'NC_000008.10',
  '9':'NC_000009.11',
  '10':'NC_000010.10',
  '11':'NC_000011.9',
  '12':'NC_000012.11',
  '13':'NC_000013.10',
  '14':'NC_000014.8',
  '15':'NC_000015.9',
  '16':'NC_000016.9',
  '17':'NC_000017.10',
  '18':'NC_000018.9',
  '19':'NC_000019.9',
  '20':'NC_000020.10',
  '21':'NC_000021.8',
  '22':'NC_000022.10',
  'X':'NC_000023.10',
  'Y':'NC_000024.9',
  'MT':'NC_01290.1',
  'M':'NC_01290.1'
  },'grch38':{
  '1':'NC_000001.11',
  '2':'NC_000002.12',
  '3':'NC_000003.12',
  '4':'NC_000004.12',
  '5':'NC_000005.10',
  '6':'NC_000006.12',
  '7':'NC_000007.14',
  '8':'NC_000008.11',
  '9':'NC_000009.12',
  '10':'NC_000010.11',
  '11':'NC_000011.10',
  '12':'NC_000012.12',
  '13':'NC_000013.11',
  '14':'NC_000014.9',
  '15':'NC_000015.10',
  '16':'NC_000016.10',
  '17':'NC_000017.11',
  '18':'NC_000018.10',
  '19':'NC_000019.10',
  '20':'NC_000020.11',
  '21':'NC_000021.9',
  '22':'NC_000022.11',
  'X':'NC_000023.11',
  'Y':'NC_000024.10',
  'MT':'NC_01290.1',
  'M':'NC_01290.1'
  }
}


class SeqRepo(DataSource):
  def __init__(self, baseurl, assembly, chr_aliases=seqrepo_aliases):
    self.baseurl = baseurl 
    self.assembly =  assembly
    self.chr_aliases = chr_aliases

  def get_chrom_alias(self, chrom):
      aliases = self.chr_aliases
      if chrom in aliases.values():
        return chrom
      if chrom.startswith('chr'):
        chrom = chrom.replace('chr', '')
      if chrom in aliases.values():
        return chrom
      try:
        return self.chr_aliases[self.assembly][chrom]
      except KeyError as e:
        return chrom

  def get_reference_seq(self, chrom, start, end):
    """
    SeqRepo http request to return reference sequence
    :param chrom:
    :param start:
    :param end:
    :return: dna reference sequence
    """
    if chrom.startswith('chr'):
        chrom = chrom.replace('chr', '')
    request = '{}/seqrepo/1/sequence/{}?start={}&end={}'.format(self.baseurl, chrom, start, end)
    try:
        dna = urlopen(request).read().decode('utf-8')
        print(dna)
    except (URLError, ExpatError) as e:
        print('Could not reach SeqRepo REST service. Please check that the service is running.\n{}\n{}'.format(request, str(e)))
        dna = "n" * (start - end)
    return dna


class UCSC(DataSource):
  
  def __init__(self, baseurl, assembly, chr_aliases=seqrepo_aliases):
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

