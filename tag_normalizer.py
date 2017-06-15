import re
from functools import lru_cache
from sys import intern


class TagNormalizer:
    # http://opencorpora.org/dict.php?act=gram
    # http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
    remove_re = re.compile(
        "(Abbr|Name|Surn|Patr|Geox|Orgn|Trad|Infr|Slng|Arch|Litr|Erro|Dist|Qual|Poss|Anum|Apro|Prdx|(V-(be|en|ie|bi|sh|ej|oy|ey))|Af-p|Inmx|Subx|Fixd|intg|real|Adjx|Vpre|Cmp2|Anph|incl|excl|Supr)(\s|,)?")
    plur_gender_re = re.compile('femn|masc|ms-f|GNdr')
    ms_f_re = re.compile('Ms-f(\s|,)?')

    @lru_cache()
    def normalize(self, tag: str) -> str:
        t = tag
        if 'plur' in tag:
            t = self.plur_gender_re.sub('neut', t)

        if 'Ms-f' in tag and ('femn' or 'masc' or 'neut' in tag):
            t = self.ms_f_re.sub('', t)

        #t = t.replace('intr', 'tran')
        t = t.replace('loc2', 'loct').replace('gen2', 'gent').replace('acc2', 'accs')
        t = t.replace('ANim', 'anim')

        return intern(self._remove_unnecessary(t))

    def _remove_unnecessary(self, text):
        l = len(text)
        text = self.remove_re.sub('', text)
        while l != len(text):
            l = len(text)
            text = self.remove_re.sub('', text)
        return text.replace(' ', ',').strip(' ,')
