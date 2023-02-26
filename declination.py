import spacy
import requests

nlp = spacy.load('pl_core_news_lg')

def correct_word(word):
    return word.replace('\\xc4\\x85','ą').replace('\\xc4\\x99','ę').replace('\\xc5\\x82','ł').replace('\\xc5\\x9b','ś').replace('\\xc4\\x87','ć').replace('\\xc5\\x84','ń').replace('\\xc3\\xb3','ó').replace('\\xc5\\ba','ź').replace('\\xc5\\xbc','ż')

def ret_lemma(word):
    return [token.lemma_ for token in nlp(word)][0]

def ret_declin_wiktionary(input_word, full = True):
    word = ret_lemma(input_word)
    url = 'https://en.wiktionary.org/wiki/' + word
    r = requests.get(url)
    tekst = str(r.content)
    
    if 'mianownik (kto? co?)' in tekst:
        start_mian = '<th title="mianownik (kto? co?)'
        start_dop = '<th title="dope\\xc5\\x82niacz (kogo? czego?)'    
        start_cel = '<th title="celownik (komu? czemu?)'
        start_bier = '<th title="biernik (kogo? co?)'
        start_narz = '<th title="narz\\xc4\\x99dnik (kim? czym?)'
        start_miejsc = '<th title="miejscownik (o kim? o czym?)'
        start_wol = '<th title="wo\\xc5\\x82acz (o!)'
        end = '</a>'


        def return_declin_form(start_declin_form, end):
            return tekst.split(start_declin_form)[1].split(end)[0].split('>')[-1]

        def make_declin_list(end='</a>'): 
            mian = return_declin_form(start_mian, end)            
            dop = return_declin_form(start_dop, end)            
            cel = return_declin_form(start_cel, end)            
            bier = return_declin_form(start_bier, end)            
            narz = return_declin_form(start_narz, end)            
            miejs = return_declin_form(start_miejsc, end)            
            wol = return_declin_form(start_wol, end)            
            return [mian, dop, cel, bier, narz, miejs, wol]

        declination_list = make_declin_list()
        declination_list_corr = list(map(correct_word, declination_list))

        if input_word not in declination_list_corr:
            new_end = '</a></span>\\n</td></tr>'
            declination_list = make_declin_list(end=new_end)
            declination_list_corr = list(map(correct_word, declination_list))
            
        if full:
            return declination_list_corr
        else:
            przypadki = ['mianownik', 'dopełniacz', 'celownik', 'biernik', 'narzędnik', 'miejscownik', 'wołacz']
            for n,_ in enumerate(declination_list):
                if correct_word(_) == input_word:
                    return przypadki[n]
            else:
                return False
            
            return declination_list_corr
    else:
        return False

ret_declin_wiktionary('kowadełko')
# ['kowadełko',
#  'kowadełka',
#  'kowadełku',
#  'kowadełko',
#  'kowadełkiem',
#  'kowadełku',
#  'kowadełko']

ret_declin_wiktionary('żółwiowi', full=False)
# 'celownik'