from collections import defaultdict

__all__ = ['rules', 'vocabulary', 'transforms']

vocabulary = {
    'как?': 'CONJ%ADVB,Ques',
    'где?': 'CONJ%ADVB,Ques',
    'когда?': 'CONJ%ADVB,Ques',
    'куда?': 'ADVB,Ques',
    'откуда?': 'ADVB,Ques',

    'который?': 'ADJF,Apro,masc,sing,nomn',
    'которая?': 'ADJF,Apro,femn,sing,nomn',
    'которое?': 'ADJF,Apro,neut,sing,nomn',
    'которые?': 'ADJF,Apro,plur,nomn',

    'которого?': 'ADJF,Apro,masc,sing,gent',
    'которой?': 'ADJF,Apro,femn,sing,gent',
    'которого?*': 'ADJF,Apro,neut,sing,gent',
    'которых?': 'ADJF,Apro,plur,gent',

    'которому?': 'ADJF,Apro,masc,sing,datv',
    'которой?*': 'ADJF,Apro,femn,sing,datv',
    'которому?*': 'ADJF,Apro,neut,sing,datv',
    'которым?': 'ADJF,Apro,plur,datv',

    'которого?**': 'ADJF,Apro,anim,masc,sing,accs',
    'который?*': 'ADJF,Apro,inan,masc,sing,accs',
    'которую?': 'ADJF,Apro,femn,sing,accs',
    'которое?*': 'ADJF,Apro,neut,sing,accs',
    'которых?*': 'ADJF,Apro,anim,plur,accs',
    'которые?*': 'ADJF,Apro,inan,plur,accs',

    'которым?*': 'ADJF,Apro,masc,sing,ablt',
    'которой?**': 'ADJF,Apro,femn,sing,ablt',
    'которым?**': 'ADJF,Apro,neut,sing,ablt',
    'которыми?': 'ADJF,Apro,plur,ablt',

    'котором?': 'ADJF,Apro,masc,sing,loct',
    'которой?***': 'ADJF,Apro,femn,sing,loct',
    'котором?*': 'ADJF,Apro,neut,sing,loct',
    'которых?**': 'ADJF,Apro,plur,loct',

    'сколько?': 'NUMR,nomn',
    'скольких?': 'NUMR,gent',
    'скольким?': 'NUMR,datv',
    'скольких?*': 'NUMR,anim,accs',
    'сколько?*': 'NUMR,inan,accs',
    'сколькими?': 'NUMR,ablt',
    'скольких?**': 'NUMR,loct',

    'кто?': 'NPRO,masc,sing,nomn',
    'что?': 'CONJ%NPRO,neut,sing,nomn%ADVB,Ques',

    'кого?': 'NPRO,masc,sing,accs',
    'чего?': 'NPRO,neut,sing,gent',

    'кому?': 'NPRO,masc,sing,datv',
    'чему?': 'NPRO,neut,sing,datv',

    'кого?*': 'NPRO,masc,sing,accs',
    'что?*': 'NPRO,neut,sing,accs',

    'кем?': 'NPRO,masc,sing,ablt',
    'чем?': 'NPRO,neut,sing,ablt',

    'ком?': 'NPRO,masc,sing,loct',
    'чём?': 'NPRO,neut,sing,loct',

    'чей?': 'ADJF,Apro,masc,sing,nomn',
    'чья?': 'ADJF,Apro,femn,sing,nomn',
    'чьё?': 'ADJF,Apro,neut,sing,nomn',
    'чьи?': 'ADJF,Apro,plur,nomn',

    'чьего?': 'ADJF,Apro,masc,sing,gent',
    'чьей?': 'ADJF,Apro,femn,sing,gent',
    'чьего?*': 'ADJF,Apro,neut,sing,gent',
    'чьих?': 'ADJF,Apro,plur,gent',

    'чьему?': 'ADJF,Apro,masc,sing,datv',
    'чьей?*': 'ADJF,Apro,femn,sing,datv',
    'чьему?*': 'ADJF,Apro,neut,sing,datv',
    'чьим?': 'ADJF,Apro,plur,datv',

    'чьего?**': 'ADJF,Apro,anim,masc,sing,accs',
    'чей?*': 'ADJF,Apro,inan,masc,sing,accs',
    'чью?': 'ADJF,Apro,femn,sing,accs',
    'чьё?*': 'ADJF,Apro,neut,sing,accs',
    'чьих?*': 'ADJF,Apro,anim,plur,accs',
    'чьи?*': 'ADJF,Apro,inan,plur,accs',

    'чьим?*': 'ADJF,Apro,masc,sing,ablt',
    'чьей?**': 'ADJF,Apro,femn,sing,ablt',
    'чьим?**': 'ADJF,Apro,neut,sing,ablt',
    'чьими?': 'ADJF,Apro,plur,ablt',

    'чьём?': 'ADJF,Apro,masc,sing,loct',
    'чьей?***': 'ADJF,Apro,femn,sing,loct',
    'чьём?*': 'ADJF,Apro,neut,sing,loct',
    'чьих?**': 'ADJF,Apro,plur,loct',

    'какой?': 'ADJF,Apro,masc,sing,nomn',
    'какая?': 'ADJF,Apro,femn,sing,nomn',
    'какое?': 'ADJF,Apro,neut,sing,nomn',
    'какие?': 'ADJF,Apro,plur,nomn',

    'какого?': 'ADJF,Apro,masc,sing,gent',
    'какой?*': 'ADJF,Apro,femn,sing,gent',
    'какого?*': 'ADJF,Apro,neut,sing,gent',
    'каких?*': 'ADJF,Apro,plur,gent',

    'какому?': 'ADJF,Apro,masc,sing,datv',
    'какой?**': 'ADJF,Apro,femn,sing,datv',
    'какому?*': 'ADJF,Apro,neut,sing,datv',
    'каким?': 'ADJF,Apro,plur,datv',

    'какого?**': 'ADJF,Apro,anim,masc,sing,accs',
    'какой?***': 'ADJF,Apro,inan,masc,sing,accs',
    'какую?': 'ADJF,Apro,femn,sing,accs',
    'какое?*': 'ADJF,Apro,neut,sing,accs',
    'каких?**': 'ADJF,Apro,anim,plur,accs',
    'какие?*': 'ADJF,Apro,inan,plur,accs',

    'каким?*': 'ADJF,Apro,masc,sing,ablt',
    'какой?****': 'ADJF,Apro,femn,sing,ablt',
    'каким?**': 'ADJF,Apro,neut,sing,ablt',
    'какими?': 'ADJF,Apro,plur,ablt',

    'каком?': 'ADJF,Apro,masc,sing,loct',
    'какой?*****': 'ADJF,Apro,femn,sing,loct',
    'каком?*': 'ADJF,Apro,neut,sing,loct',
    'каких?': 'ADJF,Apro,plur,loct',

    'нет': 'PRED,pres',
    'о': 'PREP',
    'с': 'PREP',
    'на': 'PREP',
    'очень': 'ADVB',
    'холодно': 'ADVB',
    'и': 'CONJ',
    ',': 'PNCT',

    #########################################################
    'без': 'PREP',
    'не': 'PRCL',
    'некогда': 'PRED,pres',
    'светлее': 'COMP',

    'камень': 'NOUN,inan,masc,sing,nomn',
    'ветка': 'NOUN,inan,femn,sing,nomn',
    'дерево': 'NOUN,inan,neut,sing,nomn',
    'камни': 'NOUN,inan,neut,plur,nomn',

    'камня': 'NOUN,inan,masc,sing,gent',
    'ветки': 'NOUN,inan,femn,sing,gent',
    'дерева': 'NOUN,inan,neut,sing,gent',
    'камней': 'NOUN,inan,neut,plur,gent',

    'камню': 'NOUN,inan,masc,sing,datv',
    'ветке': 'NOUN,inan,femn,sing,datv',
    'дереву': 'NOUN,inan,neut,sing,datv',
    'камням': 'NOUN,inan,neut,plur,datv',

    'кирпич': 'NOUN,inan,masc,sing,accs',
    'ветку': 'NOUN,inan,femn,sing,accs',
    'полено': 'NOUN,inan,neut,sing,accs',
    'кирпичи': 'NOUN,inan,neut,plur,accs',

    'камнем': 'NOUN,inan,masc,sing,ablt',
    'веткой': 'NOUN,inan,femn,sing,ablt',
    'деревом': 'NOUN,inan,neut,sing,ablt',
    'камнями': 'NOUN,inan,neut,plur,ablt',

    'камне': 'NOUN,inan,masc,sing,loct',
    'палке': 'NOUN,inan,femn,sing,loct',
    'дереве': 'NOUN,inan,neut,sing,loct',
    'камнях': 'NOUN,inan,neut,plur,loct',

    'кот': 'NOUN,anim,masc,sing,nomn',
    'девочка': 'NOUN,anim,femn,sing,nomn',
    'создание': 'NOUN,anim,neut,sing,nomn',
    'коты': 'NOUN,anim,neut,plur,nomn',

    'кота': 'NOUN,anim,masc,sing,gent',
    'девочки': 'NOUN,anim,femn,sing,gent',
    'создания': 'NOUN,anim,neut,sing,gent',
    'котов': 'NOUN,anim,neut,plur,gent',

    'коту': 'NOUN,anim,masc,sing,datv',
    'девочке': 'NOUN,anim,femn,sing,datv',
    'созданию': 'NOUN,anim,neut,sing,datv',
    'котам': 'NOUN,anim,neut,plur,datv',

    'пса': 'NOUN,anim,masc,sing,accs',
    'девочку': 'NOUN,anim,femn,sing,accs',
    'создание*': 'NOUN,anim,neut,sing,accs',
    'собак': 'NOUN,anim,neut,plur,accs',

    'котом': 'NOUN,anim,masc,sing,ablt',
    'девочкой': 'NOUN,anim,femn,sing,ablt',
    'созданием': 'NOUN,anim,neut,sing,ablt',
    'котами': 'NOUN,anim,neut,plur,ablt',

    'коте': 'NOUN,anim,masc,sing,loct',
    'собаке': 'NOUN,anim,femn,sing,loct',
    'создании**': 'NOUN,anim,neut,sing,loct',
    'котах': 'NOUN,anim,neut,plur,loct',

    'я': 'NPRO,1per,sing,nomn',
    'мы': 'NPRO,1per,plur,nomn',

    'ты': 'NPRO,2per,sing,nomn',
    'вы': 'NPRO,2per,plur,nomn',

    'он': 'NPRO,masc,3per,sing,nomn',
    'она': 'NPRO,femn,3per,sing,nomn',
    'оно': 'NPRO,neut,3per,sing,nomn',
    'они': 'NPRO,3per,plur,nomn',

    'меня': 'NPRO,1per,sing,gent',
    'нас': 'NPRO,1per,plur,gent',

    'тебя': 'NPRO,2per,sing,gent',
    'вас': 'NPRO,2per,plur,gent',

    'его': 'NPRO,masc,3per,sing,gent',
    'её': 'NPRO,femn,3per,sing,gent',
    'него': 'NPRO,neut,3per,sing,gent',
    'их': 'NPRO,3per,plur,gent',

    'мне': 'NPRO,1per,sing,datv',
    'нам': 'NPRO,1per,plur,datv',

    'тебе': 'NPRO,2per,sing,datv',
    'вам': 'NPRO,2per,plur,datv',

    'ему': 'NPRO,masc,3per,sing,datv',
    'ей': 'NPRO,femn,3per,sing,datv',
    'нему': 'NPRO,neut,3per,sing,datv',
    'им': 'NPRO,3per,plur,datv',

    'меня*': 'NPRO,1per,sing,accs',
    'нас*': 'NPRO,1per,plur,accs',

    'тебя*': 'NPRO,2per,sing,accs',
    'вас*': 'NPRO,2per,plur,accs',

    'его*': 'NPRO,masc,3per,sing,accs',
    'её*': 'NPRO,femn,3per,sing,accs',
    'него*': 'NPRO,neut,3per,sing,accs',
    'их*': 'NPRO,3per,plur,accs',

    'мной': 'NPRO,1per,sing,ablt',
    'нами': 'NPRO,1per,plur,ablt',

    'тобой': 'NPRO,2per,sing,ablt',
    'вами': 'NPRO,2per,plur,ablt',

    'им*': 'NPRO,masc,3per,sing,ablt',
    'ей*': 'NPRO,femn,3per,sing,ablt',
    'им**': 'NPRO,neut,3per,sing,ablt',
    'ими': 'NPRO,3per,plur,ablt',

    'мне**': 'NPRO,1per,sing,loct',
    'нас**': 'NPRO,1per,plur,loct',

    'тебе**': 'NPRO,2per,sing,loct',
    'вас**': 'NPRO,2per,plur,loct',

    'нём': 'NPRO,masc,3per,sing,loct',
    'ней': 'NPRO,femn,3per,sing,loct',
    'нём*': 'NPRO,neut,3per,sing,loct',
    'них': 'NPRO,3per,plur,loct',

    'жёлт': 'ADJS,masc,sing',  #
    'жёлто': 'ADJS,neut,sing',  #
    'желта': 'ADJS,femn,sing',  #
    'жёлты': 'ADJS,plur',  #

    'синий': 'ADJF,masc,sing,nomn',
    'синяя': 'ADJF,femn,sing,nomn',
    'красное': 'ADJF,neut,sing,nomn',
    'синие': 'ADJF,plur,nomn',

    'синего': 'ADJF,masc,sing,gent',
    'синей': 'ADJF,femn,sing,gent',
    'красного': 'ADJF,neut,sing,gent',
    'синих': 'ADJF,plur,gent',

    'синему': 'ADJF,masc,sing,datv',
    'зелёной': 'ADJF,femn,sing,datv',
    'красному': 'ADJF,neut,sing,datv',
    'синим': 'ADJF,plur,datv',

    'зелёного': 'ADJF,anim,masc,sing,accs',
    'зелёный': 'ADJF,inan,masc,sing,accs',
    'зелёную': 'ADJF,femn,sing,accs',
    'жёлтое': 'ADJF,neut,sing,accs',
    'жёлтых': 'ADJF,anim,plur,accs',
    'жёлтые': 'ADJF,inan,plur,accs',

    'синим*': 'ADJF,masc,sing,ablt',
    'жёлтой': 'ADJF,femn,sing,ablt',
    'красным': 'ADJF,neut,sing,ablt',
    'синими': 'ADJF,plur,ablt',

    'синем': 'ADJF,masc,sing,loct',
    'белой': 'ADJF,femn,sing,loct',
    'красном': 'ADJF,neut,sing,loct',
    'красных': 'ADJF,plur,loct',

    'два': 'NUMR,masc,nomn',
    'две': 'NUMR,femn,nomn',
    'два**': 'NUMR,neut,nomn',
    'десять': 'NUMR,nomn',

    'двух': 'NUMR,masc,gent',
    'двух*': 'NUMR,femn,gent',
    'двух**': 'NUMR,neut,gent',
    'десяти': 'NUMR,gent',

    'двум': 'NUMR,masc,datv',
    'двум*': 'NUMR,femn,datv',
    'двум**': 'NUMR,neut,datv',
    'девяти': 'NUMR,datv',

    'два*': 'NUMR,inan,masc,accs',
    'двух***': 'NUMR,anim,masc,accs',
    'две*': 'NUMR,inan,femn,accs',
    'двух****': 'NUMR,anim,femn,accs',
    'два***': 'NUMR,neut,accs',
    'девять': 'NUMR,accs',
    'четырёх': 'NUMR,anim,accs',
    'четыре': 'NUMR,inan,accs',

    'двумя': 'NUMR,masc,ablt',
    'двумя*': 'NUMR,femn,ablt',
    'двумя**': 'NUMR,neut,ablt',
    'десятью': 'NUMR,ablt',

    'двух*****': 'NUMR,masc,loct',
    'двух******': 'NUMR,femn,loct',
    'двух*******': 'NUMR,neut,loct',
    'восьми': 'NUMR,loct',

    'медленно': 'ADVB',

    'давить': 'INFN,impf,tran',

    'давил': 'VERB,impf,tran,masc,sing,past,indc',
    'давила': 'VERB,impf,tran,femn,sing,past,indc',
    'давило': 'VERB,impf,tran,neut,sing,past,indc',
    'давили': 'VERB,impf,tran,plur,past,indc',

    'давлю': 'VERB,impf,tran,sing,1per,pres,indc',
    'давим': 'VERB,impf,tran,plur,1per,pres,indc',
    'давишь': 'VERB,impf,tran,sing,2per,pres,indc',
    'давите': 'VERB,impf,tran,plur,2per,pres,indc',
    'давит': 'VERB,impf,tran,sing,3per,pres,indc',
    'давят': 'VERB,impf,tran,plur,3per,pres,indc',

    'буду_давить': 'VERB,impf,intr,sing,1per,futr,indc|INFN,impf,tran',
    'будем_давить': 'VERB,impf,intr,plur,1per,futr,indc|INFN,impf,tran',
    'будешь_давить': 'VERB,impf,intr,sing,2per,futr,indc|INFN,impf,tran',
    'будете_давить': 'VERB,impf,intr,plur,2per,futr,indc|INFN,impf,tran',
    'будет_давить': 'VERB,impf,intr,sing,3per,futr,indc|INFN,impf,tran',
    'будут_давить': 'VERB,impf,intr,plur,3per,futr,indc|INFN,impf,tran',

    'идём': 'VERB,impf,tran,sing,impr,incl',
    'идёмте': 'VERB,impf,tran,plur,impr,incl',

    'дави': 'VERB,impf,tran,sing,impr,excl',
    'давите*': 'VERB,impf,tran,plur,impr,excl',

    'раздавить': 'INFN,perf,tran',

    'раздавил': 'VERB,perf,tran,masc,sing,past,indc',
    'раздавила': 'VERB,perf,tran,femn,sing,past,indc',
    'раздавили': 'VERB,perf,tran,plur,past,indc',
    'раздавило': 'VERB,perf,tran,neut,sing,past,indc',

    'раздавлю': 'VERB,perf,tran,sing,1per,futr,indc',
    'раздавим': 'VERB,perf,tran,plur,1per,futr,indc',
    'раздавишь': 'VERB,perf,tran,sing,2per,futr,indc',
    'раздавите': 'VERB,perf,tran,plur,2per,futr,indc',
    'раздавит': 'VERB,perf,tran,sing,3per,futr,indc',
    'раздавят': 'VERB,perf,tran,plur,3per,futr,indc',

    'поедем': 'VERB,perf,tran,sing,impr,incl',
    'поедемте': 'VERB,perf,tran,plur,impr,incl',

    'раздави': 'VERB,perf,tran,sing,impr,excl',
    'раздавите*': 'VERB,perf,tran,plur,impr,excl',

    'падать': 'INFN,impf,intr',

    'падал': 'VERB,impf,intr,masc,sing,past,indc',
    'падала': 'VERB,impf,intr,femn,sing,past,indc',
    'падало': 'VERB,impf,intr,neut,sing,past,indc',
    'падали': 'VERB,impf,intr,plur,past,indc',

    'падаю': 'VERB,impf,intr,sing,1per,pres,indc',
    'падаем': 'VERB,impf,intr,plur,1per,pres,indc',
    'падаешь': 'VERB,impf,intr,sing,2per,pres,indc',
    'падаете': 'VERB,impf,intr,plur,2per,pres,indc',
    'падает': 'VERB,impf,intr,sing,3per,pres,indc',
    'падают': 'VERB,impf,intr,plur,3per,pres,indc',

    'буду_падать': 'VERB,impf,intr,sing,1per,futr,indc|INFN,impf,intr',
    'будем_падать': 'VERB,impf,intr,plur,1per,futr,indc|INFN,impf,intr',
    'будешь_падать': 'VERB,impf,intr,sing,2per,futr,indc|INFN,impf,intr',
    'будете_падать': 'VERB,impf,intr,plur,2per,futr,indc|INFN,impf,intr',
    'будет_падать': 'VERB,impf,intr,sing,3per,futr,indc|INFN,impf,intr',
    'будут_падать': 'VERB,impf,intr,plur,3per,futr,indc|INFN,impf,intr',

    'падай': 'VERB,impf,intr,sing,impr,excl',
    'падайте': 'VERB,impf,intr,plur,impr,excl',

    'упасть': 'INFN,perf,intr',

    'упал': 'VERB,perf,intr,masc,sing,past,indc',
    'упала': 'VERB,perf,intr,femn,sing,past,indc',
    'упали': 'VERB,perf,intr,plur,past,indc',
    'упало': 'VERB,perf,intr,neut,sing,past,indc',

    'упаду': 'VERB,perf,intr,sing,1per,futr,indc',
    'упадём': 'VERB,perf,intr,plur,1per,futr,indc',
    'упадёшь': 'VERB,perf,intr,sing,2per,futr,indc',
    'упадёте': 'VERB,perf,intr,plur,2per,futr,indc',
    'упадёт': 'VERB,perf,intr,sing,3per,futr,indc',
    'упадут': 'VERB,perf,intr,plur,3per,futr,indc',

    'упади': 'VERB,perf,intr,sing,impr,excl',
    'упадите': 'VERB,perf,intr,plur,impr,excl',

    'рисующий': 'PRTF,impf,tran,pres,actv,masc,sing,nomn',
    'рисующая': 'PRTF,impf,tran,pres,actv,femn,sing,nomn',
    'рисующее': 'PRTF,impf,tran,pres,actv,neut,sing,nomn',
    'рисующие': 'PRTF,impf,tran,pres,actv,plur,nomn',

    'рисовавший': 'PRTF,impf,tran,past,actv,masc,sing,nomn',
    'рисовавшая': 'PRTF,impf,tran,past,actv,femn,sing,nomn',
    'рисовавшее': 'PRTF,impf,tran,past,actv,neut,sing,nomn',
    'рисовавшие': 'PRTF,impf,tran,past,actv,plur,nomn',

    'рисуемый': 'PRTF,impf,tran,pres,pssv,masc,sing,nomn',
    'рисуемая': 'PRTF,impf,tran,pres,pssv,femn,sing,nomn',
    'рисуемое': 'PRTF,impf,tran,pres,pssv,neut,sing,nomn',
    'рисуемые': 'PRTF,impf,tran,pres,pssv,plur,nomn',

    'рисованный': 'PRTF,impf,tran,past,pssv,masc,sing,nomn',
    'рисованная': 'PRTF,impf,tran,past,pssv,femn,sing,nomn',
    'рисованное': 'PRTF,impf,tran,past,pssv,neut,sing,nomn',
    'рисованные': 'PRTF,impf,tran,past,pssv,plur,nomn',

    'написавший': 'PRTF,perf,tran,past,actv,masc,sing,nomn',
    'написавшая': 'PRTF,perf,tran,past,actv,femn,sing,nomn',
    'написавшее': 'PRTF,perf,tran,past,actv,neut,sing,nomn',
    'написавшие': 'PRTF,perf,tran,past,actv,plur,nomn',

    'написанный': 'PRTF,perf,tran,past,pssv,masc,sing,nomn',
    'написанная': 'PRTF,perf,tran,past,pssv,femn,sing,nomn',
    'написанное': 'PRTF,perf,tran,past,pssv,neut,sing,nomn',
    'написанные': 'PRTF,perf,tran,past,pssv,plur,nomn',

    'рисующего': 'PRTF,impf,tran,pres,actv,masc,sing,gent',
    'рисующей': 'PRTF,impf,tran,pres,actv,femn,sing,gent',
    'рисующего*': 'PRTF,impf,tran,pres,actv,neut,sing,gent',
    'рисующих': 'PRTF,impf,tran,pres,actv,plur,gent',

    'рисовавшего': 'PRTF,impf,tran,past,actv,masc,sing,gent',
    'рисовавшей': 'PRTF,impf,tran,past,actv,femn,sing,gent',
    'рисовавшего*': 'PRTF,impf,tran,past,actv,neut,sing,gent',
    'рисовавших': 'PRTF,impf,tran,past,actv,plur,gent',

    'рисуемого': 'PRTF,impf,tran,pres,pssv,masc,sing,gent',
    'рисуемой': 'PRTF,impf,tran,pres,pssv,femn,sing,gent',
    'рисуемого*': 'PRTF,impf,tran,pres,pssv,neut,sing,gent',
    'рисуемых': 'PRTF,impf,tran,pres,pssv,plur,gent',

    'рисованного': 'PRTF,impf,tran,past,pssv,masc,sing,gent',
    'рисованной': 'PRTF,impf,tran,past,pssv,femn,sing,gent',
    'рисованного*': 'PRTF,impf,tran,past,pssv,neut,sing,gent',
    'рисованных': 'PRTF,impf,tran,past,pssv,plur,gent',

    'написавшего': 'PRTF,perf,tran,past,actv,masc,sing,gent',
    'написавшей': 'PRTF,perf,tran,past,actv,femn,sing,gent',
    'написавшего*': 'PRTF,perf,tran,past,actv,neut,sing,gent',
    'написавших': 'PRTF,perf,tran,past,actv,plur,gent',

    'написанного': 'PRTF,perf,tran,past,pssv,masc,sing,gent',
    'написанной': 'PRTF,perf,tran,past,pssv,femn,sing,gent',
    'написанного*': 'PRTF,perf,tran,past,pssv,neut,sing,gent',
    'написанных': 'PRTF,perf,tran,past,pssv,plur,gent',

    'рисующему': 'PRTF,impf,tran,pres,actv,masc,sing,datv',
    'рисующей*': 'PRTF,impf,tran,pres,actv,femn,sing,datv',
    'рисующему*': 'PRTF,impf,tran,pres,actv,neut,sing,datv',
    'рисующим': 'PRTF,impf,tran,pres,actv,plur,datv',

    'рисовавшему': 'PRTF,impf,tran,past,actv,masc,sing,datv',
    'рисовавшей*': 'PRTF,impf,tran,past,actv,femn,sing,datv',
    'рисовавшему*': 'PRTF,impf,tran,past,actv,neut,sing,datv',
    'рисовавшим': 'PRTF,impf,tran,past,actv,plur,datv',

    'рисуемому': 'PRTF,impf,tran,pres,pssv,masc,sing,datv',
    'рисуемой*': 'PRTF,impf,tran,pres,pssv,femn,sing,datv',
    'рисуемому*': 'PRTF,impf,tran,pres,pssv,neut,sing,datv',
    'рисуемым': 'PRTF,impf,tran,pres,pssv,plur,datv',

    'рисованному': 'PRTF,impf,tran,past,pssv,masc,sing,datv',
    'рисованной*': 'PRTF,impf,tran,past,pssv,femn,sing,datv',
    'рисованному*': 'PRTF,impf,tran,past,pssv,neut,sing,datv',
    'рисованным': 'PRTF,impf,tran,past,pssv,plur,datv',

    'написавшему': 'PRTF,perf,tran,past,actv,masc,sing,datv',
    'написавшей*': 'PRTF,perf,tran,past,actv,femn,sing,datv',
    'написавшему*': 'PRTF,perf,tran,past,actv,neut,sing,datv',
    'написавшим': 'PRTF,perf,tran,past,actv,plur,datv',

    'написанному': 'PRTF,perf,tran,past,pssv,masc,sing,datv',
    'написанной*': 'PRTF,perf,tran,past,pssv,femn,sing,datv',
    'написанному*': 'PRTF,perf,tran,past,pssv,neut,sing,datv',
    'написанным': 'PRTF,perf,tran,past,pssv,plur,datv',

    'рисующего**': 'PRTF,impf,tran,pres,actv,anim,masc,sing,accs',
    'рисующий*': 'PRTF,impf,tran,pres,actv,inan,masc,sing,accs',
    'рисующую': 'PRTF,impf,tran,pres,actv,femn,sing,accs',
    'рисующее*': 'PRTF,impf,tran,pres,actv,neut,sing,accs',
    'рисующих*': 'PRTF,impf,tran,pres,actv,anim,plur,accs',
    'рисующие*': 'PRTF,impf,tran,pres,actv,inan,plur,accs',

    'рисовавшего**': 'PRTF,impf,tran,past,actv,anim,masc,sing,accs',
    'рисовавший*': 'PRTF,impf,tran,past,actv,inan,masc,sing,accs',
    'рисовавшую': 'PRTF,impf,tran,past,actv,femn,sing,accs',
    'рисовавшее*': 'PRTF,impf,tran,past,actv,neut,sing,accs',
    'рисовавших*': 'PRTF,impf,tran,past,actv,anim,plur,accs',
    'рисовавшие*': 'PRTF,impf,tran,past,actv,inan,plur,accs',

    'рисуемого**': 'PRTF,impf,tran,pres,pssv,anim,masc,sing,accs',
    'рисуемый*': 'PRTF,impf,tran,pres,pssv,inan,masc,sing,accs',
    'рисуемую': 'PRTF,impf,tran,pres,pssv,femn,sing,accs',
    'рисуемое*': 'PRTF,impf,tran,pres,pssv,neut,sing,accs',
    'рисуемых*': 'PRTF,impf,tran,pres,pssv,anim,plur,accs',
    'рисуемые*': 'PRTF,impf,tran,pres,pssv,inan,plur,accs',

    'рисованного**': 'PRTF,impf,tran,past,pssv,anim,masc,sing,accs',
    'рисованный*': 'PRTF,impf,tran,past,pssv,inan,masc,sing,accs',
    'рисованную': 'PRTF,impf,tran,past,pssv,femn,sing,accs',
    'рисованное*': 'PRTF,impf,tran,past,pssv,neut,sing,accs',
    'рисованных*': 'PRTF,impf,tran,past,pssv,anim,plur,accs',
    'рисованные*': 'PRTF,impf,tran,past,pssv,inan,plur,accs',

    'написавшего**': 'PRTF,perf,tran,past,actv,anim,masc,sing,accs',
    'написавший*': 'PRTF,perf,tran,past,actv,inan,masc,sing,accs',
    'написавшую': 'PRTF,perf,tran,past,actv,femn,sing,accs',
    'написавшее*': 'PRTF,perf,tran,past,actv,neut,sing,accs',
    'написавших*': 'PRTF,perf,tran,past,actv,anim,plur,accs',
    'написавшие*': 'PRTF,perf,tran,past,actv,inan,plur,accs',

    'написанного**': 'PRTF,perf,tran,past,pssv,anim,masc,sing,accs',
    'написанный*': 'PRTF,perf,tran,past,pssv,inan,masc,sing,accs',
    'написанную': 'PRTF,perf,tran,past,pssv,femn,sing,accs',
    'написанное*': 'PRTF,perf,tran,past,pssv,neut,sing,accs',
    'написанных*': 'PRTF,perf,tran,past,pssv,anim,plur,accs',
    'написанные*': 'PRTF,perf,tran,past,pssv,inan,plur,accs',

    'рисующим*': 'PRTF,impf,tran,pres,actv,masc,sing,ablt',
    'рисующей**': 'PRTF,impf,tran,pres,actv,femn,sing,ablt',
    'рисующим**': 'PRTF,impf,tran,pres,actv,neut,sing,ablt',
    'рисующими': 'PRTF,impf,tran,pres,actv,plur,ablt',

    'рисовавшим*': 'PRTF,impf,tran,past,actv,masc,sing,ablt',
    'рисовавшей**': 'PRTF,impf,tran,past,actv,femn,sing,ablt',
    'рисовавшим**': 'PRTF,impf,tran,past,actv,neut,sing,ablt',
    'рисовавшими': 'PRTF,impf,tran,past,actv,plur,ablt',

    'рисуемым*': 'PRTF,impf,tran,pres,pssv,masc,sing,ablt',
    'рисуемой**': 'PRTF,impf,tran,pres,pssv,femn,sing,ablt',
    'рисуемым**': 'PRTF,impf,tran,pres,pssv,neut,sing,ablt',
    'рисуемыми': 'PRTF,impf,tran,pres,pssv,plur,ablt',

    'рисованным*': 'PRTF,impf,tran,past,pssv,masc,sing,ablt',
    'рисованной**': 'PRTF,impf,tran,past,pssv,femn,sing,ablt',
    'рисованным**': 'PRTF,impf,tran,past,pssv,neut,sing,ablt',
    'рисованными': 'PRTF,impf,tran,past,pssv,plur,ablt',

    'написавшим*': 'PRTF,perf,tran,past,actv,masc,sing,ablt',
    'написавшей**': 'PRTF,perf,tran,past,actv,femn,sing,ablt',
    'написавшим**': 'PRTF,perf,tran,past,actv,neut,sing,ablt',
    'написавшими': 'PRTF,perf,tran,past,actv,plur,ablt',

    'написанным*': 'PRTF,perf,tran,past,pssv,masc,sing,ablt',
    'написанной**': 'PRTF,perf,tran,past,pssv,femn,sing,ablt',
    'написанным**': 'PRTF,perf,tran,past,pssv,neut,sing,ablt',
    'написанными': 'PRTF,perf,tran,past,pssv,plur,ablt',

    'рисующем': 'PRTF,impf,tran,pres,actv,masc,sing,loct',
    'рисующей***': 'PRTF,impf,tran,pres,actv,femn,sing,loct',
    'рисующем*': 'PRTF,impf,tran,pres,actv,neut,sing,loct',
    'рисующих**': 'PRTF,impf,tran,pres,actv,plur,loct',

    'рисовавшем': 'PRTF,impf,tran,past,actv,masc,sing,loct',
    'рисовавшей***': 'PRTF,impf,tran,past,actv,femn,sing,loct',
    'рисовавшем*': 'PRTF,impf,tran,past,actv,neut,sing,loct',
    'рисовавших**': 'PRTF,impf,tran,past,actv,plur,loct',

    'рисуемом': 'PRTF,impf,tran,pres,pssv,masc,sing,loct',
    'рисуемой***': 'PRTF,impf,tran,pres,pssv,femn,sing,loct',
    'рисуемом*': 'PRTF,impf,tran,pres,pssv,neut,sing,loct',
    'рисуемых**': 'PRTF,impf,tran,pres,pssv,plur,loct',

    'рисованном': 'PRTF,impf,tran,past,pssv,masc,sing,loct',
    'рисованной***': 'PRTF,impf,tran,past,pssv,femn,sing,loct',
    'рисованном*': 'PRTF,impf,tran,past,pssv,neut,sing,loct',
    'рисованных**': 'PRTF,impf,tran,past,pssv,plur,loct',

    'написавшем': 'PRTF,perf,tran,past,actv,masc,sing,loct',
    'написавшей***': 'PRTF,perf,tran,past,actv,femn,sing,loct',
    'написавшем*': 'PRTF,perf,tran,past,actv,neut,sing,loct',
    'написавших**': 'PRTF,perf,tran,past,actv,plur,loct',

    'написанном': 'PRTF,perf,tran,past,pssv,masc,sing,loct',
    'написанной***': 'PRTF,perf,tran,past,pssv,femn,sing,loct',
    'написанном*': 'PRTF,perf,tran,past,pssv,neut,sing,loct',
    'написанных**': 'PRTF,perf,tran,past,pssv,plur,loct',

    'рисуем': 'PRTS,impf,pres,pssv,masc,sing',
    'рисуема': 'PRTS,impf,pres,pssv,femn,sing',
    'рисуемо': 'PRTS,impf,pres,pssv,neut,sing',
    'рисуемы': 'PRTS,impf,pres,pssv,plur',

    'рисован': 'PRTS,impf,past,pssv,masc,sing',
    'рисована': 'PRTS,impf,past,pssv,femn,sing',
    'рисовано': 'PRTS,impf,past,pssv,neut,sing',
    'рисованы': 'PRTS,impf,past,pssv,plur',

    'написан': 'PRTS,perf,past,pssv,masc,sing',
    'написана': 'PRTS,perf,past,pssv,femn,sing',
    'написано': 'PRTS,perf,past,pssv,neut,sing',
    'написаны': 'PRTS,perf,past,pssv,plur',

    'написав': 'GRND,perf,tran past',
    'давя': 'GRND,impf,tran pres',
    'давив': 'GRND,impf,tran past',

    'падающий': 'PRTF,impf,intr,pres,actv,masc,sing,nomn',
    'падающая': 'PRTF,impf,intr,pres,actv,femn,sing,nomn',
    'падающее': 'PRTF,impf,intr,pres,actv,neut,sing,nomn',
    'падающие': 'PRTF,impf,intr,pres,actv,plur,nomn',

    'падавший': 'PRTF,impf,intr,past,actv,masc,sing,nomn',
    'падавшая': 'PRTF,impf,intr,past,actv,femn,sing,nomn',
    'падавшее': 'PRTF,impf,intr,past,actv,neut,sing,nomn',
    'падавшие': 'PRTF,impf,intr,past,actv,plur,nomn',

    'упавший': 'PRTF,perf,intr,past,actv,masc,sing,nomn',
    'упавшая': 'PRTF,perf,intr,past,actv,femn,sing,nomn',
    'упавшее': 'PRTF,perf,intr,past,actv,neut,sing,nomn',
    'упавшие': 'PRTF,perf,intr,past,actv,plur,nomn',

    'падающего': 'PRTF,impf,intr,pres,actv,masc,sing,gent',
    'падающей': 'PRTF,impf,intr,pres,actv,femn,sing,gent',
    'падающего*': 'PRTF,impf,intr,pres,actv,neut,sing,gent',
    'падающих': 'PRTF,impf,intr,pres,actv,plur,gent',

    'падавшего': 'PRTF,impf,intr,past,actv,masc,sing,gent',
    'падавшей': 'PRTF,impf,intr,past,actv,femn,sing,gent',
    'падавшего*': 'PRTF,impf,intr,past,actv,neut,sing,gent',
    'падавших': 'PRTF,impf,intr,past,actv,plur,gent',

    'упавшего': 'PRTF,perf,intr,past,actv,masc,sing,gent',
    'упавшей': 'PRTF,perf,intr,past,actv,femn,sing,gent',
    'упавшего*': 'PRTF,perf,intr,past,actv,neut,sing,gent',
    'упавших': 'PRTF,perf,intr,past,actv,plur,gent',

    'падающему': 'PRTF,impf,intr,pres,actv,masc,sing,datv',
    'падающей*': 'PRTF,impf,intr,pres,actv,femn,sing,datv',
    'падающему*': 'PRTF,impf,intr,pres,actv,neut,sing,datv',
    'падающим': 'PRTF,impf,intr,pres,actv,plur,datv',

    'падавшему': 'PRTF,impf,intr,past,actv,masc,sing,datv',
    'падавшей*': 'PRTF,impf,intr,past,actv,femn,sing,datv',
    'падавшему*': 'PRTF,impf,intr,past,actv,neut,sing,datv',
    'падавшим': 'PRTF,impf,intr,past,actv,plur,datv',

    'упавшему': 'PRTF,perf,intr,past,actv,masc,sing,datv',
    'упавшей*': 'PRTF,perf,intr,past,actv,femn,sing,datv',
    'упавшему*': 'PRTF,perf,intr,past,actv,neut,sing,datv',
    'упавшим': 'PRTF,perf,intr,past,actv,plur,datv',

    'падающего**': 'PRTF,impf,intr,pres,actv,anim,masc,sing,accs',
    'падающий*': 'PRTF,impf,intr,pres,actv,inan,masc,sing,accs',
    'падающую': 'PRTF,impf,intr,pres,actv,femn,sing,accs',
    'падающее*': 'PRTF,impf,intr,pres,actv,neut,sing,accs',
    'падающих*': 'PRTF,impf,intr,pres,actv,anim,plur,accs',
    'падающие*': 'PRTF,impf,intr,pres,actv,inan,plur,accs',

    'падавшего**': 'PRTF,impf,intr,past,actv,anim,masc,sing,accs',
    'падавший*': 'PRTF,impf,intr,past,actv,inan,masc,sing,accs',
    'падавшую': 'PRTF,impf,intr,past,actv,femn,sing,accs',
    'падавшее*': 'PRTF,impf,intr,past,actv,neut,sing,accs',
    'падавших*': 'PRTF,impf,intr,past,actv,anim,plur,accs',
    'падавшие*': 'PRTF,impf,intr,past,actv,inan,plur,accs',

    'упавшего**': 'PRTF,perf,intr,past,actv,anim,masc,sing,accs',
    'упавший*': 'PRTF,perf,intr,past,actv,inan,masc,sing,accs',
    'упавшую': 'PRTF,perf,intr,past,actv,femn,sing,accs',
    'упавшее*': 'PRTF,perf,intr,past,actv,neut,sing,accs',
    'упавших*': 'PRTF,perf,intr,past,actv,anim,plur,accs',
    'упавшие*': 'PRTF,perf,intr,past,actv,inan,plur,accs',

    'падающим*': 'PRTF,impf,intr,pres,actv,masc,sing,ablt',
    'падающей**': 'PRTF,impf,intr,pres,actv,femn,sing,ablt',
    'падающим**': 'PRTF,impf,intr,pres,actv,neut,sing,ablt',
    'падающими': 'PRTF,impf,intr,pres,actv,plur,ablt',

    'падавшим*': 'PRTF,impf,intr,past,actv,masc,sing,ablt',
    'падавшей**': 'PRTF,impf,intr,past,actv,femn,sing,ablt',
    'падавшим**': 'PRTF,impf,intr,past,actv,neut,sing,ablt',
    'падавшими': 'PRTF,impf,intr,past,actv,plur,ablt',

    'упавшим*': 'PRTF,perf,intr,past,actv,masc,sing,ablt',
    'упавшей**': 'PRTF,perf,intr,past,actv,femn,sing,ablt',
    'упавшим**': 'PRTF,perf,intr,past,actv,neut,sing,ablt',
    'упавшими': 'PRTF,perf,intr,past,actv,plur,ablt',

    'падающем': 'PRTF,impf,intr,pres,actv,masc,sing,loct',
    'падающей***': 'PRTF,impf,intr,pres,actv,femn,sing,loct',
    'падающем*': 'PRTF,impf,intr,pres,actv,neut,sing,loct',
    'падающих**': 'PRTF,impf,intr,pres,actv,plur,loct',

    'падавшем': 'PRTF,impf,intr,past,actv,masc,sing,loct',
    'падавшей***': 'PRTF,impf,intr,past,actv,femn,sing,loct',
    'падавшем*': 'PRTF,impf,intr,past,actv,neut,sing,loct',
    'падавших**': 'PRTF,impf,intr,past,actv,plur,loct',

    'упавшем': 'PRTF,perf,intr,past,actv,masc,sing,loct',
    'упавшей***': 'PRTF,perf,intr,past,actv,femn,sing,loct',
    'упавшем*': 'PRTF,perf,intr,past,actv,neut,sing,loct',
    'упавших**': 'PRTF,perf,intr,past,actv,plur,loct',

    'упав': 'GRND,perf,intr,past',
    'падая': 'GRND,impf,intr,pres',
    'падав': 'GRND,impf,intr,past',
}

transforms = {

    'какой?': {'какие?', 'какая?', 'какое?'},
    'какая?': {'какие?', 'какой?', 'какое?'},
    'какое?': {'какие?', 'какой?', 'какая?'},
    'какие?': {'какой?', 'какая?', 'какое?'},

    'какого?': {'каких?*', 'какой?*', 'какого?*'},
    'какой?*': {'каких?*', 'какого?', 'какого?*'},
    'какого?*': {'каких?*', 'какого?', 'какой?*'},
    'каких?*': {'какого?', 'какой?*', 'какого?*'},

    'какому?': {'каким?', 'какой?**', 'какому?*'},
    'какой?**': {'каким?', 'какому?', 'какому?*'},
    'какому?*': {'каким?', 'какому?', 'какой?**'},
    'каким?': {'какому?', 'какой?**', 'какому?*'},

    'какого?**': {'каких?**', 'какую?', 'какое?*'},
    'какой?***': {'какие?*', 'какую?', 'какое?*'},
    'какую?': {'каких?**', 'какие?*', 'какого?**', 'какой?***', 'какое?*'},
    'какое?*': {'каких?**', 'какие?*', 'какого?**', 'какой?***', 'какую?'},
    'каких?**': {'какого?**'},
    'какие?*': {'какой?***'},

    'каким?*': {'какими?', 'какой?****', 'каким?**'},
    'какой?****': {'какими?', 'каким?*', 'каким?**'},
    'каким?**': {'какими?', 'каким?*', 'какой?****'},
    'какими?': {'каким?*', 'какой?****', 'каким?**'},

    'каком?': {'каких?', 'какой?*****', 'каком?*'},
    'какой?*****': {'каких?', 'каком?', 'каком?*'},
    'каком?*': {'каких?', 'каком?', 'какой?*****'},
    'каких?': {'каком?', 'какой?*****', 'каком?*'},

    'который?': {'которые?', 'которая?', 'которое?'},
    'которая?': {'которые?', 'который?', 'которое?'},
    'которое?': {'которые?', 'который?', 'которая?'},
    'которые?': {'который?', 'которая?', 'которое?'},

    'которого?': {'которых?', 'которой?', 'которого?*'},
    'которой?': {'которых?', 'которого?', 'которого?*'},
    'которого?*': {'которых?', 'которого?', 'которой?'},
    'которых?': {'которого?', 'которой?', 'которого?*'},

    'которому?': {'которым?', 'которой?*', 'которому?*'},
    'которой?*': {'которым?', 'которому?', 'которому?*'},
    'которому?*': {'которым?', 'которому?', 'которой?*'},
    'которым?': {'которому?', 'которой?*', 'которому?*'},

    'которого?**': {'которых?*', 'которую?', 'которое?*'},
    'который?*': {'которые?*', 'которую?', 'которое?*'},
    'которую?': {'которых?*', 'которые?*', 'которого?**', 'который?*', 'которое?*'},
    'которое?*': {'которых?*', 'которые?*', 'которого?**', 'который?*', 'которую?'},
    'которых?*': {'которого?**'},
    'которые?*': {'который?*'},

    'которым?*': {'которыми?', 'которой?**', 'которым?**'},
    'которой?**': {'которыми?', 'которым?*', 'которым?**'},
    'которым?**': {'которыми?', 'которым?*', 'которой?**'},
    'которыми?': {'которым?*', 'которой?**', 'которым?**'},

    'котором?': {'которых?**', 'которой?***', 'котором?*'},
    'которой?***': {'которых?**', 'котором?', 'котором?*'},
    'котором?*': {'которых?**', 'котором?', 'которой?***'},
    'которых?**': {'котором?', 'которой?***', 'котором?*'},

    'чей?': {'чьи?', 'чья?', 'чьё?'},
    'чья?': {'чьи?', 'чей?', 'чьё?'},
    'чьё?': {'чьи?', 'чей?', 'чья?'},
    'чьи?': {'чей?', 'чья?', 'чьё?'},

    'чьего?': {'чьих?', 'чьей?', 'чьего?*'},
    'чьей?': {'чьих?', 'чьего?', 'чьего?*'},
    'чьего?*': {'чьих?', 'чьего?', 'чьей?'},
    'чьих?': {'чьего?', 'чьей?', 'чьего?*'},

    'чьему?': {'чьим?', 'чьей?*', 'чьему?*'},
    'чьей?*': {'чьим?', 'чьему?', 'чьему?*'},
    'чьему?*': {'чьим?', 'чьему?', 'чьей?*'},
    'чьим?': {'чьему?', 'чьей?*', 'чьему?*'},

    'чьего?**': {'чьих?*', 'чью?', 'чьё?*'},
    'чей?*': {'чьи?*', 'чью?', 'чьё?*'},
    'чью?': {'чьих?*', 'чьи?*', 'чьего?**', 'чей?*', 'чьё?*'},
    'чьё?*': {'чьих?*', 'чьи?*', 'чьего?**', 'чей?*', 'чью?'},
    'чьих?*': {'чьего?**'},
    'чьи?*': {'чей?*'},

    'чьим?*': {'чьими?', 'чьей?**', 'чьим?**'},
    'чьей?**': {'чьими?', 'чьим?*', 'чьим?**'},
    'чьим?**': {'чьими?', 'чьим?*', 'чьей?**'},
    'чьими?': {'чьим?*', 'чьей?**', 'чьим?**'},

    'чьём?': {'чьих?**', 'чьей?***', 'чьём?*'},
    'чьей?***': {'чьих?**', 'чьём?', 'чьём?*'},
    'чьём?*': {'чьих?**', 'чьём?', 'чьей?***'},
    'чьих?**': {'чьём?', 'чьей?***', 'чьём?*'},

    #######################################
    'камень': {'камни', 'ветка', 'дерево'},
    'ветка': {'камни', 'камень', 'дерево'},
    'дерево': {'камни', 'камень', 'ветка'},
    'камни': {'камень'},

    'камня': {'камней', 'ветки', 'дерева'},
    'ветки': {'камней', 'камня', 'дерева'},
    'дерева': {'камней', 'камня', 'ветки'},
    'камней': {'камня'},

    'камню': {'камням', 'ветке', 'дереву'},
    'ветке': {'камням', 'камню', 'дереву'},
    'дереву': {'камням', 'камню', 'ветке'},
    'камням': {'камню'},

    'кирпич': {'кирпичи', 'ветку', 'полено'},
    'ветку': {'кирпичи', 'кирпич', 'полено'},
    'полено': {'кирпичи', 'кирпич', 'ветку'},
    'кирпичи': {'кирпич'},

    'камнем': {'камнями', 'веткой', 'деревом'},
    'веткой': {'камнями', 'камнем', 'деревом'},
    'деревом': {'камнями', 'камнем', 'веткой'},
    'камнями': {'камнем'},

    'камне': {'камнях', 'палке', 'дереве'},
    'палке': {'камнях', 'камне', 'дереве'},
    'дереве': {'камнях', 'камне', 'палке'},
    'камнях': {'камне'},

    'кот': {'коты', 'девочка', 'создание'},
    'девочка': {'коты', 'кот', 'создание'},
    'создание': {'коты', 'кот', 'девочка'},
    'коты': {'кот'},

    'кота': {'котов', 'девочки', 'создания'},
    'девочки': {'котов', 'кота', 'создания'},
    'создания': {'котов', 'кота', 'девочки'},
    'котов': {'кота'},

    'коту': {'котам', 'девочке', 'созданию'},
    'девочке': {'котам', 'коту', 'созданию'},
    'созданию': {'котам', 'коту', 'девочке'},
    'котам': {'коту'},

    'пса': {'собак', 'девочку', 'создание*'},
    'девочку': {'собак', 'пса', 'создание*'},
    'создание*': {'собак', 'пса', 'девочку'},
    'собак': {'пса'},

    'котом': {'котами', 'девочкой', 'созданием'},
    'девочкой': {'котами', 'котом', 'созданием'},
    'созданием': {'котами', 'котом', 'девочкой'},
    'котами': {'котом'},

    'коте': {'котах', 'собаке', 'создании**'},
    'собаке': {'котах', 'коте', 'создании**'},
    'создании**': {'котах', 'коте', 'собаке'},
    'котах': {'коте'},

    'я': {'мы', 'ты', 'он', 'она', 'оно'},
    'мы': {'я', 'вы', 'они'},
    'ты': {'вы', 'я', 'он', 'она', 'оно'},
    'вы': {'ты', 'мы', 'они'},
    'он': {'они', 'она', 'оно', 'кот'},
    'она': {'они', 'он', 'оно', 'девочка'},
    'оно': {'они', 'она', 'он', 'создание'},
    'они': {'он', 'она', 'оно', 'коты'},

    'меня': {'нас', 'тебя', 'его', 'её', 'него'},
    'нас': {'меня', 'вас', 'их'},
    'тебя': {'вас', 'меня', 'его', 'её', 'него'},
    'вас': {'тебя', 'нас', 'их'},
    'его': {'их', 'её', 'него', 'кота'},
    'её': {'их', 'его', 'него', 'девочки'},
    'него': {'их', 'её', 'его', 'создания'},
    'их': {'его', 'её', 'него', 'котов'},

    'мне': {'нам', 'тебя', 'ему', 'ей', 'нему'},
    'нам': {'мне', 'вы', 'они'},
    'тебе': {'вам', 'мне', 'ему', 'ей', 'нему'},
    'вам': {'тебе', 'нам', 'им'},
    'ему': {'им', 'ей', 'нему', 'коту'},
    'ей': {'им', 'ему', 'нему', 'девочке'},
    'нему': {'им', 'ей', 'ему', 'созданию'},
    'им': {'ему', 'ей', 'нему', 'котам'},

    'меня*': {'нас*', 'тебя*', 'его*', 'её*', 'него*'},
    'нас*': {'меня*', 'вас*', 'их*'},
    'тебя*': {'вас*', 'меня*', 'его*', 'её*', 'него*'},
    'вас*': {'тебя*', 'нас*', 'их*'},
    'его*': {'их*', 'её*', 'него*', 'пса'},
    'её*': {'их*', 'его*', 'него*', 'девочку'},
    'него*': {'их*', 'её*', 'его*', 'создание*'},
    'их*': {'его*', 'её*', 'него*', 'собак'},

    'мной': {'нами', 'тобой', 'им*', 'ей*', 'им**'},
    'нами': {'мной', 'вами', 'ими'},
    'тобой': {'вами', 'мной', 'им*', 'ей*', 'им**'},
    'вами': {'тобой', 'нами', 'ими'},
    'им*': {'ими', 'ей*', 'им**', 'котом'},
    'ей*': {'ими', 'им*', 'им**', 'девочкой'},
    'им**': {'ими', 'ей*', 'им*', 'созданием'},
    'ими': {'им*', 'ей*', 'им**', 'котами'},

    'мне**': {'нас**', 'тебе**', 'нём', 'ней', 'нём*'},
    'нас**': {'мне**', 'вас**', 'них'},
    'тебе**': {'вас**', 'мне**', 'нём', 'ней', 'нём*'},
    'вас**': {'тебе**', 'нас**', 'них'},
    'нём': {'них', 'ней', 'нём*', 'коте'},
    'ней': {'них', 'нём', 'нём*', 'собаке'},
    'нём*': {'них', 'ней', 'нём', 'создании**'},
    'них': {'нём', 'ней', 'нём*', 'котах'},

    'жёлт': {'жёлты', 'желта', 'жёлто'},
    'желта': {'жёлты', 'жёлт', 'жёлто'},
    'жёлто': {'жёлты', 'жёлт', 'желта'},
    'жёлты': {'жёлт', 'желта', 'жёлто'},

    'синий': {'синие', 'синяя', 'красное'},
    'синяя': {'синие', 'синий', 'красное'},
    'красное': {'синие', 'синий', 'синяя'},
    'синие': {'синий', 'синяя', 'красное'},

    'синего': {'синих', 'синей', 'красного'},
    'синей': {'синих', 'синего', 'красного'},
    'красного': {'синих', 'синего', 'синей'},
    'синих': {'синего', 'синей', 'красного'},

    'синему': {'синим', 'зелёной', 'красному'},
    'зелёной': {'синим', 'синему', 'красному'},
    'красному': {'синим', 'синему', 'зелёной'},
    'синим': {'синему', 'зелёной', 'красному'},

    'зелёного': {'жёлтых', 'зелёную', 'жёлтое'},
    'зелёный': {'жёлтые', 'зелёную', 'жёлтое'},
    'зелёную': {'жёлтых', 'жёлтые', 'зелёного', 'зелёный', 'жёлтое'},
    'жёлтое': {'жёлтых', 'жёлтые', 'зелёного', 'зелёный', 'зелёную'},
    'жёлтых': {'зелёного'},
    'жёлтые': {'зелёный'},

    'синим*': {'синими', 'жёлтой', 'красным'},
    'жёлтой': {'синими', 'синим*', 'красным'},
    'красным': {'синими', 'синим*', 'жёлтой'},
    'синими': {'синим*', 'жёлтой', 'красным'},

    'синем': {'красных', 'белой', 'красном'},
    'белой': {'красных', 'синем', 'красном'},
    'красном': {'красных', 'синем', 'белой'},
    'красных': {'синем', 'белой', 'красном'},

    'рисующий': {'рисующие', 'рисующая', 'рисующее', 'рисовавший'},
    'рисующая': {'рисующие', 'рисующий', 'рисующее', 'рисовавшая'},
    'рисующее': {'рисующие', 'рисующий', 'рисующая', 'рисовавшее'},
    'рисующие': {'рисующий', 'рисующая', 'рисующее', 'рисовавшие'},

    'рисовавший': {'рисовавшие', 'рисовавшая', 'рисовавшее', 'рисующий'},
    'рисовавшая': {'рисовавшие', 'рисовавший', 'рисовавшее', 'рисующая'},
    'рисовавшее': {'рисовавшие', 'рисовавший', 'рисовавшая', 'рисующее'},
    'рисовавшие': {'рисовавший', 'рисовавшая', 'рисовавшее', 'рисующие'},

    'рисуемый': {'рисуемые', 'рисуемая', 'рисуемое', 'рисованный'},
    'рисуемая': {'рисуемые', 'рисуемый', 'рисуемое', 'рисованная'},
    'рисуемое': {'рисуемые', 'рисуемый', 'рисуемая', 'рисованное'},
    'рисуемые': {'рисуемый', 'рисуемая', 'рисуемое', 'рисованные'},

    'рисованный': {'рисованные', 'рисованная', 'рисованное', 'рисуемый'},
    'рисованная': {'рисованные', 'рисованный', 'рисованное', 'рисуемая'},
    'рисованное': {'рисованные', 'рисованный', 'рисованная', 'рисуемое'},
    'рисованные': {'рисованный', 'рисованная', 'рисованное', 'рисуемые'},

    'рисующего': {'рисующих', 'рисующей', 'рисующего*', 'рисовавшего'},
    'рисующей': {'рисующих', 'рисующего', 'рисующего*', 'рисовавшей'},
    'рисующего*': {'рисующих', 'рисующего', 'рисующей', 'рисовавшего*'},
    'рисующих': {'рисующего', 'рисующей', 'рисующего*', 'рисовавших'},

    'рисовавшего': {'рисовавших', 'рисовавшей', 'рисовавшего*', 'рисующего'},
    'рисовавшей': {'рисовавших', 'рисовавшего', 'рисовавшего*', 'рисующей'},
    'рисовавшего*': {'рисовавших', 'рисовавшего', 'рисовавшей', 'рисующего*'},
    'рисовавших': {'рисовавшего', 'рисовавшей', 'рисовавшего*', 'рисующих'},

    'рисуемого': {'рисуемых', 'рисуемой', 'рисуемого*', 'рисованного'},
    'рисуемой': {'рисуемых', 'рисуемого', 'рисуемого*', 'рисованной'},
    'рисуемого*': {'рисуемых', 'рисуемого', 'рисуемой', 'рисованного*'},
    'рисуемых': {'рисуемого', 'рисуемой', 'рисуемого*', 'рисованных'},

    'рисованного': {'рисованных', 'рисованной', 'рисованного*', 'рисуемого'},
    'рисованной': {'рисованных', 'рисованного', 'рисованного*', 'рисуемой'},
    'рисованного*': {'рисованных', 'рисованного', 'рисованной', 'рисуемого*'},
    'рисованных': {'рисованного', 'рисованной', 'рисованного*', 'рисуемых'},

    'рисующему': {'рисующим', 'рисующей*', 'рисующему*', 'рисовавшему'},
    'рисующей*': {'рисующим', 'рисующему', 'рисующему*', 'рисовавшей*'},
    'рисующему*': {'рисующим', 'рисующему', 'рисующей*', 'рисовавшему*'},
    'рисующим': {'рисующему', 'рисующей*', 'рисующему*', 'рисовавшим'},

    'рисовавшему': {'рисовавшим', 'рисовавшей*', 'рисовавшему*', 'рисующему'},
    'рисовавшей*': {'рисовавшим', 'рисовавшему', 'рисовавшему*', 'рисующей*'},
    'рисовавшему*': {'рисовавшим', 'рисовавшему', 'рисовавшей*', 'рисующему*'},
    'рисовавшим': {'рисовавшему', 'рисовавшей*', 'рисовавшему*', 'рисующим'},

    'рисуемому': {'рисуемым', 'рисуемой*', 'рисуемому*', 'рисованному'},
    'рисуемой*': {'рисуемым', 'рисуемому', 'рисуемому*', 'рисованной*'},
    'рисуемому*': {'рисуемым', 'рисуемому', 'рисуемой*', 'рисованному*'},
    'рисуемым': {'рисуемому', 'рисуемой*', 'рисуемому*', 'рисованным'},

    'рисованному': {'рисованным', 'рисованной*', 'рисованному*', 'рисуемому'},
    'рисованной*': {'рисованным', 'рисованному', 'рисованному*', 'рисуемой*'},
    'рисованному*': {'рисованным', 'рисованному', 'рисованной*', 'рисуемому*'},
    'рисованным': {'рисованному', 'рисованной*', 'рисованному*', 'рисуемым'},

    'рисующего**': {'рисующих*', 'рисующую', 'рисующее*', 'рисовавшего**'},
    'рисующий*': {'рисующие*', 'рисующую', 'рисующее*', 'рисовавший*'},
    'рисующую': {'рисующих*', 'рисующие*', 'рисующего**', 'рисующий*', 'рисующее*', 'рисовавшую'},
    'рисующее*': {'рисующих*', 'рисующие*', 'рисующего**', 'рисующий*', 'рисующую', 'рисовавшее*'},
    'рисующих*': {'рисующего**', 'рисовавших*'},
    'рисующие*': {'рисующий*', 'рисовавшие*'},

    'рисовавшего**': {'рисовавших*', 'рисовавшую', 'рисовавшее*', 'рисующего**'},
    'рисовавший*': {'рисовавшие*', 'рисовавшую', 'рисовавшее*', 'рисующий*'},
    'рисовавшую': {'рисовавших*', 'рисовавшие*', 'рисовавшего**', 'рисовавший*', 'рисовавшее*', 'рисующую'},
    'рисовавшее*': {'рисовавших*', 'рисовавшие*', 'рисовавшего**', 'рисовавший*', 'рисовавшую', 'рисующее*'},
    'рисовавших*': {'рисовавшего**', 'рисующих*'},
    'рисовавшие*': {'рисовавший*', 'рисующие*'},

    'рисуемого**': {'рисуемых*', 'рисуемую', 'рисуемое*', 'рисованного**'},
    'рисуемый*': {'рисуемые*', 'рисуемую', 'рисуемое*', 'рисованный*'},
    'рисуемую': {'рисуемых*', 'рисуемые*', 'рисуемого**', 'рисуемый*', 'рисуемое*', 'рисованную'},
    'рисуемое*': {'рисуемых*', 'рисуемые*', 'рисуемого**', 'рисуемый*', 'рисуемую', 'рисованное*'},
    'рисуемых*': {'рисуемого**', 'рисованных*'},
    'рисуемые*': {'рисуемый*', 'рисованные*'},

    'рисованного**': {'рисованных*', 'рисованную', 'рисованное*', 'рисуемого**'},
    'рисованный*': {'рисованные*', 'рисованную', 'рисованное*', 'рисуемый*'},
    'рисованную': {'рисованных*', 'рисованные*', 'рисованного**', 'рисованный*', 'рисованное*', 'рисуемую'},
    'рисованное*': {'рисованных*', 'рисованные*', 'рисованного**', 'рисованный*', 'рисованную', 'рисуемое*'},
    'рисованных*': {'рисованного**', 'рисуемых*'},
    'рисованные*': {'рисованный*', 'рисуемые*'},

    'рисующим*': {'рисующими', 'рисующей**', 'рисующим**', 'рисовавшим*'},
    'рисующей**': {'рисующими', 'рисующим*', 'рисующим**', 'рисовавшей**'},
    'рисующим**': {'рисующими', 'рисующим*', 'рисующей**', 'рисовавшим**'},
    'рисующими': {'рисующим*', 'рисующей**', 'рисующим**', 'рисовавшими'},

    'рисовавшим*': {'рисовавшими', 'рисовавшей**', 'рисовавшим**', 'рисующим*'},
    'рисовавшей**': {'рисовавшими', 'рисовавшим*', 'рисовавшим**', 'рисующей**'},
    'рисовавшим**': {'рисовавшими', 'рисовавшим*', 'рисовавшей**', 'рисующим**'},
    'рисовавшими': {'рисовавшим*', 'рисовавшей**', 'рисовавшим**', 'рисующими'},

    'рисуемым*': {'рисуемыми', 'рисуемой**', 'рисуемым**', 'рисованным*'},
    'рисуемой**': {'рисуемыми', 'рисуемым*', 'рисуемым**', 'рисованной**'},
    'рисуемым**': {'рисуемыми', 'рисуемым*', 'рисуемой**', 'рисованным**'},
    'рисуемыми': {'рисуемым*', 'рисуемой**', 'рисуемым**', 'рисованными'},

    'рисованным*': {'рисованными', 'рисованной**', 'рисованным**', 'рисуемым*'},
    'рисованной**': {'рисованными', 'рисованным*', 'рисованным**', 'рисуемой**'},
    'рисованным**': {'рисованными', 'рисованным*', 'рисованной**', 'рисуемым**'},
    'рисованными': {'рисованным*', 'рисованной**', 'рисованным**', 'рисуемыми'},

    'рисующем': {'рисующих**', 'рисующей***', 'рисующем*', 'рисовавшем'},
    'рисующей***': {'рисующих**', 'рисующем', 'рисующем*', 'рисовавшей***'},
    'рисующем*': {'рисующих**', 'рисующем', 'рисующей***', 'рисовавшем*'},
    'рисующих**': {'рисующем', 'рисующей***', 'рисующем*', 'рисовавших**'},

    'рисовавшем': {'рисовавших**', 'рисовавшей***', 'рисовавшем*', 'рисующем'},
    'рисовавшей***': {'рисовавших**', 'рисовавшем', 'рисовавшем*', 'рисующей***'},
    'рисовавшем*': {'рисовавших**', 'рисовавшем', 'рисовавшей***', 'рисующем*'},
    'рисовавших**': {'рисовавшем', 'рисовавшей***', 'рисовавшем*', 'рисующих**'},

    'рисуемом': {'рисуемых**', 'рисуемой***', 'рисуемом*', 'рисованном'},
    'рисуемой***': {'рисуемых**', 'рисуемом', 'рисуемом*', 'рисованной***'},
    'рисуемом*': {'рисуемых**', 'рисуемом', 'рисуемой***', 'рисованном*'},
    'рисуемых**': {'рисуемом', 'рисуемой***', 'рисуемом*', 'рисованных**'},

    'рисованном': {'рисованных**', 'рисованной***', 'рисованном*', 'рисуемом'},
    'рисованной***': {'рисованных**', 'рисованном', 'рисованном*', 'рисуемой***'},
    'рисованном*': {'рисованных**', 'рисованном', 'рисованной***', 'рисуемом*'},
    'рисованных**': {'рисованном', 'рисованной***', 'рисованном*', 'рисуемых**'},

    'рисуем': {'рисуемы', 'рисуема', 'рисуемо'},
    'рисуема': {'рисуемы', 'рисуем', 'рисуемо'},
    'рисуемо': {'рисуемы', 'рисуем', 'рисуема'},
    'рисуемы': {'рисуем', 'рисуема', 'рисуемо'},

    'рисован': {'рисованы', 'рисована', 'рисовано'},
    'рисована': {'рисованы', 'рисован', 'рисовано'},
    'рисовано': {'рисованы', 'рисован', 'рисована'},
    'рисованы': {'рисован', 'рисована', 'рисовано'},

    'написавший': {'написавшие', 'написавшая', 'написавшее'},
    'написавшая': {'написавшие', 'написавший', 'написавшее'},
    'написавшее': {'написавшие', 'написавший', 'написавшая'},
    'написавшие': {'написавший', 'написавшая', 'написавшее'},

    'написанный': {'написанные', 'написанная', 'написанное'},
    'написанная': {'написанные', 'написанный', 'написанное'},
    'написанное': {'написанные', 'написанный', 'написанная'},
    'написанные': {'написанный', 'написанная', 'написанное'},

    'написавшего': {'написавших', 'написавшей', 'написавшего*'},
    'написавшей': {'написавших', 'написавшего', 'написавшего*'},
    'написавшего*': {'написавших', 'написавшего', 'написавшей'},
    'написавших': {'написавшего', 'написавшей', 'написавшего*'},

    'написанного': {'написанных', 'написанной', 'написанного*'},
    'написанной': {'написанных', 'написанного', 'написанного*'},
    'написанного*': {'написанных', 'написанного', 'написанной'},
    'написанных': {'написанного', 'написанной', 'написанного*'},

    'написавшему': {'написавшим', 'написавшей*', 'написавшему*'},
    'написавшей*': {'написавшим', 'написавшему', 'написавшему*'},
    'написавшему*': {'написавшим', 'написавшему', 'написавшей*'},
    'написавшим': {'написавшему', 'написавшей*', 'написавшему*'},

    'написанному': {'написанным', 'написанной*', 'написанному*'},
    'написанной*': {'написанным', 'написанному', 'написанному*'},
    'написанному*': {'написанным', 'написанному', 'написанной*'},
    'написанным': {'написанному', 'написанной*', 'написанному*'},

    'написавшего**': {'написавших*', 'написавшую', 'написавшее*'},
    'написавший*': {'написавшие*', 'написавшую', 'написавшее*'},
    'написавшую': {'написавших*', 'написавшие*', 'написавшего**', 'написавший*', 'написавшее*'},
    'написавшее*': {'написавших*', 'написавшие*', 'написавшего**', 'написавший*', 'написавшую'},
    'написавших*': {'написавшего**'},
    'написавшие*': {'написавший*'},

    'написанного**': {'написанных*', 'написанную', 'написанное*'},
    'написанный*': {'написанные*', 'написанную', 'написанное*'},
    'написанную': {'написанных*', 'написанные*', 'написанного**', 'написанный*', 'написанное*'},
    'написанное*': {'написанных*', 'написанные*', 'написанного**', 'написанный*', 'написанную'},
    'написанных*': {'написанного**'},
    'написанные*': {'написанный*'},

    'написавшим*': {'написавшими', 'написавшей**', 'написавшим**'},
    'написавшей**': {'написавшими', 'написавшим*', 'написавшим**'},
    'написавшим**': {'написавшими', 'написавшим*', 'написавшей**'},
    'написавшими': {'написавшим*', 'написавшей**', 'написавшим**'},

    'написанным*': {'написанными', 'написанной**', 'написанным**'},
    'написанной**': {'написанными', 'написанным*', 'написанным**'},
    'написанным**': {'написанными', 'написанным*', 'написанной**'},
    'написанными': {'написанным*', 'написанной**', 'написанным**'},

    'написавшем': {'написавших**', 'написавшей***', 'написавшем*'},
    'написавшей***': {'написавших**', 'написавшем', 'написавшем*'},
    'написавшем*': {'написавших**', 'написавшем', 'написавшей***'},
    'написавших**': {'написавшем', 'написавшей***', 'написавшем*'},

    'написанном': {'написанных**', 'написанной***', 'написанном*'},
    'написанной***': {'написанных**', 'написанном', 'написанном*'},
    'написанном*': {'написанных**', 'написанном', 'написанной***'},
    'написанных**': {'написанном', 'написанной***', 'написанном*'},

    'написан': {'написаны', 'написана', 'написано'},
    'написана': {'написаны', 'написан', 'написано'},
    'написано': {'написаны', 'написан', 'написана'},
    'написаны': {'написан', 'написана', 'написано'},

    'падающий': {'падающие', 'падающая', 'падающее', 'падавший'},
    'падающая': {'падающие', 'падающий', 'падающее', 'падавшая'},
    'падающее': {'падающие', 'падающий', 'падающая', 'падавшее'},
    'падающие': {'падающий', 'падающая', 'падающее', 'падавшие'},

    'падавший': {'падавшие', 'падавшая', 'падавшее', 'падающий'},
    'падавшая': {'падавшие', 'падавший', 'падавшее', 'падающая'},
    'падавшее': {'падавшие', 'падавший', 'падавшая', 'падающее'},
    'падавшие': {'падавший', 'падавшая', 'падавшее', 'падающие'},

    'падающего': {'падающих', 'падающей', 'падающего*', 'падавшего'},
    'падающей': {'падающих', 'падающего', 'падающего*', 'падавшей'},
    'падающего*': {'падающих', 'падающего', 'падающей', 'падавшего*'},
    'падающих': {'падающего', 'падающей', 'падающего*', 'падавших'},

    'падавшего': {'падавших', 'падавшей', 'падавшего*', 'падающего'},
    'падавшей': {'падавших', 'падавшего', 'падавшего*', 'падающей'},
    'падавшего*': {'падавших', 'падавшего', 'падавшей', 'падающего*'},
    'падавших': {'падавшего', 'падавшей', 'падавшего*', 'падающих'},

    'падающему': {'падающим', 'падающей*', 'падающему*', 'падавшему'},
    'падающей*': {'падающим', 'падающему', 'падающему*', 'падавшей*'},
    'падающему*': {'падающим', 'падающему', 'падающей*', 'падавшему*'},
    'падающим': {'падающему', 'падающей*', 'падающему*', 'падавшим'},

    'падавшему': {'падавшим', 'падавшей*', 'падавшему*', 'падающему'},
    'падавшей*': {'падавшим', 'падавшему', 'падавшему*', 'падающей*'},
    'падавшему*': {'падавшим', 'падавшему', 'падавшей*', 'падающему*'},
    'падавшим': {'падавшему', 'падавшей*', 'падавшему*', 'падающим'},

    'падающего**': {'падающих*', 'падающую', 'падающее*', 'падавшего**'},
    'падающий*': {'падающие*', 'падающую', 'падающее*', 'падавший*'},
    'падающую': {'падающих*', 'падающие*', 'падающего**', 'падающий*', 'падающее*', 'падавшую'},
    'падающее*': {'падающих*', 'падающие*', 'падающего**', 'падающий*', 'падающую', 'падавшее*'},
    'падающих*': {'падающего**', 'падавших*'},
    'падающие*': {'падающий*', 'падавшие*'},

    'падавшего**': {'падавших*', 'падавшую', 'падавшее*', 'падающего**'},
    'падавший*': {'падавшие*', 'падавшую', 'падавшее*', 'падающий*'},
    'падавшую': {'падавших*', 'падавшие*', 'падавшего**', 'падавший*', 'падавшее*', 'падающую'},
    'падавшее*': {'падавших*', 'падавшие*', 'падавшего**', 'падавший*', 'падавшую', 'падающее*'},
    'падавших*': {'падавшего**', 'падающих*'},
    'падавшие*': {'падавший*', 'падающие*'},

    'падающим*': {'падающими', 'падающей**', 'падающим**', 'падавшим*'},
    'падающей**': {'падающими', 'падающим*', 'падающим**', 'падавшей**'},
    'падающим**': {'падающими', 'падающим*', 'падающей**', 'падавшим**'},
    'падающими': {'падающим*', 'падающей**', 'падающим**', 'падавшими'},

    'падавшим*': {'падавшими', 'падавшей**', 'падавшим**', 'падающим*'},
    'падавшей**': {'падавшими', 'падавшим*', 'падавшим**', 'падающей**'},
    'падавшим**': {'падавшими', 'падавшим*', 'падавшей**', 'падающим**'},
    'падавшими': {'падавшим*', 'падавшей**', 'падавшим**', 'падающими'},

    'падающем': {'падающих**', 'падающей***', 'падающем*', 'падавшем'},
    'падающей***': {'падающих**', 'падающем', 'падающем*', 'падавшей***'},
    'падающем*': {'падающих**', 'падающем', 'падающей***', 'падавшем*'},
    'падающих**': {'падающем', 'падающей***', 'падающем*', 'падавших**'},

    'падавшем': {'падавших**', 'падавшей***', 'падавшем*', 'падающем'},
    'падавшей***': {'падавших**', 'падавшем', 'падавшем*', 'падающей***'},
    'падавшем*': {'падавших**', 'падавшем', 'падавшей***', 'падающем*'},
    'падавших**': {'падавшем', 'падавшей***', 'падавшем*', 'падающих**'},

    'упавший': {'упавшие', 'упавшая', 'упавшее'},
    'упавшая': {'упавшие', 'упавший', 'упавшее'},
    'упавшее': {'упавшие', 'упавший', 'упавшая'},
    'упавшие': {'упавший', 'упавшая', 'упавшее'},

    'упавшего': {'упавших', 'упавшей', 'упавшего*'},
    'упавшей': {'упавших', 'упавшего', 'упавшего*'},
    'упавшего*': {'упавших', 'упавшего', 'упавшей'},
    'упавших': {'упавшего', 'упавшей', 'упавшего*'},

    'упавшему': {'упавшим', 'упавшей*', 'упавшему*'},
    'упавшей*': {'упавшим', 'упавшему', 'упавшему*'},
    'упавшему*': {'упавшим', 'упавшему', 'упавшей*'},
    'упавшим': {'упавшему', 'упавшей*', 'упавшему*'},

    'упавшего**': {'упавших*', 'упавшую', 'упавшее*'},
    'упавший*': {'упавшие*', 'упавшую', 'упавшее*'},
    'упавшую': {'упавших*', 'упавшие*', 'упавшего**', 'упавший*', 'упавшее*'},
    'упавшее*': {'упавших*', 'упавшие*', 'упавшего**', 'упавший*', 'упавшую'},
    'упавших*': {'упавшего**'},
    'упавшие*': {'упавший*'},

    'упавшим*': {'упавшими', 'упавшей**', 'упавшим**'},
    'упавшей**': {'упавшими', 'упавшим*', 'упавшим**'},
    'упавшим**': {'упавшими', 'упавшим*', 'упавшей**'},
    'упавшими': {'упавшим*', 'упавшей**', 'упавшим**'},

    'упавшем': {'упавших**', 'упавшей***', 'упавшем*'},
    'упавшей***': {'упавших**', 'упавшем', 'упавшем*'},
    'упавшем*': {'упавших**', 'упавшем', 'упавшей***'},
    'упавших**': {'упавшем', 'упавшей***', 'упавшем*'},

    'два': {'две', 'два**', 'десять'},
    'две': {'два', 'два**', 'десять'},
    'два**': {'две', 'два', 'десять'},
    'десять': {'два', 'две', 'два**'},

    'двух': {'двух*', 'двух**', 'десяти'},
    'двух*': {'двух', 'двух**', 'десяти'},
    'двух**': {'двух*', 'двух', 'десяти'},
    'десяти': {'двух', 'двух*', 'двух**'},

    'двум': {'двум*', 'двум**', 'девяти'},
    'двум*': {'двум', 'двум**', 'девяти'},
    'двум**': {'двум*', 'двум', 'девяти'},
    'девяти': {'двум', 'двум*', 'двум**'},

    'два*': {'двух***', 'две*', 'двух****', 'два***', 'девять'},
    'двух***': {'два*', 'две*', 'двух****', 'два***', 'девять'},
    'две*': {'два*', 'двух***', 'двух****', 'два***', 'девять'},
    'двух****': {'два*', 'двух***', 'две*', 'два***', 'девять'},
    'два***': {'два*', 'двух***', 'две*', 'двух****', 'девять'},
    'девять': {'два*', 'двух***', 'две*', 'двух****', 'два***'},

    'двумя': {'двумя*', 'двумя**', 'десятью'},
    'двумя*': {'двумя', 'двумя**', 'десятью'},
    'двумя**': {'двумя*', 'двумя', 'десятью'},
    'десятью': {'двумя', 'двумя*', 'двумя**'},

    'двух*****': {'двух******', 'двух*******', 'восьми'},
    'двух******': {'двух*****', 'двух*******', 'восьми'},
    'двух*******': {'двух******', 'двух*****', 'восьми'},
    'восьми': {'двух*****', 'двух******', 'двух*******'},

    'давил': {'давили', 'давила', 'давило', 'давит', 'будет_давить', 'давлю', 'буду_давить', 'давишь',
              'будешь_давить'},
    'давила': {'давили', 'давил', 'давило', 'давит', 'будет_давить'},
    'давило': {'давили', 'давил', 'давила', 'давит', 'будет_давить'},
    'давит': {'давят', 'давил', 'давила', 'давило', 'будет_давить'},
    'будет_давить': {'будут_давить', 'давил', 'давила', 'давило', 'давит'},
    'давили': {'давил', 'давила', 'давило', 'давят', 'будут_давить', 'давим', 'будем_давить', 'давите',
               'будете_давить'},
    'давят': {'давит', 'давили', 'будут_давить'},
    'будут_давить': {'будет_давить', 'давили', 'давят'},
    'давлю': {'давим', 'давил', 'буду_давить'},
    'буду_давить': {'будем_давить', 'давил', 'давлю'},
    'давишь': {'давите', 'давил', 'будешь_давить'},
    'будешь_давить': {'будете_давить', 'давил', 'давишь'},
    'давим': {'давлю', 'давили', 'будем_давить'},
    'будем_давить': {'буду_давить', 'давили', 'давим'},
    'давите': {'давишь', 'давили', 'будете_давить'},
    'будете_давить': {'будешь_давить', 'давили', 'давите'},
    'дави': {'давите*'},
    'давите*': {'дави'},
    'идём': {'идёмте'},
    'идёмте': {'идём'},

    'раздавил': {'раздавили', 'раздавила', 'раздавило', 'раздавит', 'раздавлю', 'раздавишь'},
    'раздавила': {'раздавили', 'раздавил', 'раздавило', 'раздавит'},
    'раздавило': {'раздавили', 'раздавил', 'раздавила', 'раздавит'},
    'раздавит': {'раздавят', 'раздавил', 'раздавила', 'раздавило'},
    'раздавили': {'раздавят', 'раздавил', 'раздавила', 'раздавило', 'раздавим', 'раздавите'},
    'раздавят': {'раздавили', 'раздавит'},
    'раздавлю': {'раздавим', 'раздавил'},
    'раздавишь': {'раздавите', 'раздавил'},
    'раздавим': {'раздавлю', 'раздавили'},
    'раздавите': {'раздавишь', 'раздавили'},
    'раздави': {'раздавите*'},
    'раздавите*': {'раздави'},
    'поедем': {'поедемте'},
    'поедемте': {'поедем'},

    'падал': {'падали', 'падала', 'падало', 'падает', 'будет_падать', 'падаю', 'буду_падать', 'падаешь',
              'будешь_падать'},
    'падала': {'падали', 'падал', 'падало', 'падает', 'будет_падать'},
    'падало': {'падали', 'падал', 'падала', 'падает', 'будет_падать'},
    'падает': {'падают', 'падал', 'падала', 'падало', 'будет_падать'},
    'будет_падать': {'будут_падать', 'падал', 'падала', 'падало', 'падает'},
    'падали': {'падал', 'падала', 'падало', 'падают', 'будут_падать', 'падаем', 'будем_падать', 'падаете',
               'будете_падать'},
    'падают': {'падает', 'падали', 'будут_падать'},
    'будут_падать': {'будет_падать', 'падали', 'падают'},
    'падаю': {'падаем', 'падал', 'буду_падать'},
    'буду_падать': {'будем_падать', 'падал', 'падаю'},
    'падаешь': {'падаете', 'падал', 'будешь_падать'},
    'будешь_падать': {'будете_падать', 'падал', 'падаешь'},
    'падаем': {'падаю', 'падали', 'будем_падать'},
    'будем_падать': {'буду_падать', 'падали', 'падаем'},
    'падаете': {'падаешь', 'падали', 'будете_падать'},
    'будете_падать': {'будешь_падать', 'падали', 'падаете'},
    'падай': {'падайте'},
    'падайте': {'падай'},

    'упал': {'упали', 'упала', 'упало', 'упадёт', 'упаду', 'упадёшь'},
    'упала': {'упали', 'упал', 'упало', 'упадёт'},
    'упало': {'упали', 'упал', 'упала', 'упадёт'},
    'упадёт': {'упадут', 'упал', 'упала', 'упало'},
    'упали': {'упадут', 'упал', 'упала', 'упало', 'упадём', 'упадёте'},
    'упадут': {'упали', 'упадёт'},
    'упаду': {'упадём', 'упал'},
    'упадёшь': {'упадёте', 'упал'},
    'упадём': {'упаду', 'упали'},
    'упадёте': {'упадёшь', 'упали'},
    'упади': {'упадите'},
    'упадите': {'упади'},
}

_rules = {

    # verb
    ('давить#^и&^,',): {'давить'},
    ('^кот#давит#^и&^,',): {'давит'},
    ('^кот#давил#^и&^,',): {'давил'},
    ('^девочка#давила#^и&^,',): {'давила'},
    ('^создание#давило#^и&^,',): {'давило'},
    ('^коты#давили#^и&^,',): {'давили'},
    ('^коты#давят#^и&^,',): {'давят'},
    ('раздавить#^и&^,',): {'раздавить'},
    ('^кот#раздавил#^и&^,',): {'раздавил'},
    ('^кот#раздавит#^и&^,',): {'раздавит'},
    ('^девочка#раздавила#^и&^,',): {'раздавила'},
    ('^создание#раздавило#^и&^,',): {'раздавило'},
    ('^коты#раздавили#^и&^,',): {'раздавили'},
    ('^коты#раздавят#^и&^,',): {'раздавят'},
    ('падать#^и&^,',): {'падать'},
    ('^кот#падал#^и&^,',): {'падал'},
    ('^девочка#падала#^и&^,',): {'падала'},
    ('^создание#падало#^и&^,',): {'падало'},
    ('^коты#падали#^и&^,',): {'падали'},
    ('^коты#падают#^и&^,',): {'падают'},
    ('упасть#^и&^,',): {'упасть'},
    ('^кот#упал#^и&^,',): {'упал'},
    ('^кот#упадёт#^и&^,',): {'упадёт'},
    ('^девочка#упала#^и&^,',): {'упала'},
    ('^создание#упало#^и&^,',): {'упало'},
    ('^коты#упали#^и&^,',): {'упали'},
    ('^коты#упадут#^и&^,',): {'упадут'},

    ('кто?', 'как?#^кот&^камень&^он', 'где?#^медленно', 'когда?#^кот&^камень&^он', 'куда?#^кот&^камень&^он',
     'откуда?#^кот&^камень&^он', '$очень&^очень#медленно',
     '$очень&^очень#холодно',):
        {'^медленно&$не#будет_давить#$кот&$камень&$он', '^медленно&$не#давил#$кот&$камень&$он',
         '^медленно&$не#давит#$кот&$камень&$он', '^медленно&$не#раздавил#$кот&$камень&$он',
         '^медленно&$не#раздавит#$кот&$камень&$он', '^медленно&$не#будет_падать#$кот&$камень&$он',
         '^медленно&$не#падал#$кот&$камень&$он', '^медленно&$не#падает#$кот&$камень&$он',
         '^медленно&$не#упал#$кот&$камень&$он', '^медленно&$не#упадёт#$кот&$камень&$он'},

    ('камень#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'кот#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'он#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',):
        {'^медленно&$не#будет_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#давил#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#давит#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавил#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавит#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#будет_падать#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падал#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падает#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упал#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упадёт#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи'},

    ('как?#^девочка&^ветка&^она', 'куда?#^девочка&^ветка&^она', 'откуда?#^девочка&^ветка&^она', 'где?#^медленно',
     'когда?#^девочка&^ветка&^она', '$очень&^очень#медленно',
     '$очень&^очень#холодно',):
        {'^медленно&$не#давила#$девочка&$ветка&$она', '^медленно&$не#давит#$девочка&$ветка&$она',
         '^медленно&$не#будет_давить#$девочка&$ветка&$она', '^медленно&$не#раздавила#$девочка&$ветка&$она',
         '^медленно&$не#раздавит#$девочка&$ветка&$она', '^медленно&$не#падала#$девочка&$ветка&$она',
         '^медленно&$не#падает#$девочка&$ветка&$она', '^медленно&$не#будет_падать#$девочка&$ветка&$она',
         '^медленно&$не#упала#$девочка&$ветка&$она', '^медленно&$не#упадёт#$девочка&$ветка&$она'},

    ('ветка#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'девочка#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'она#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',):
        {'^медленно&$не#давила#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#давит#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#будет_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавила#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавит#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падала#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падает#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#будет_падать#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упала#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упадёт#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи'},

    ('как?#^создание&^дерево&^оно', 'куда?#^создание&^дерево&^оно', 'откуда?#^создание&^дерево&^оно', 'где?#^медленно',
     'когда?#^создание&^дерево&^оно', '$очень&^очень#медленно',
     '$очень&^очень#холодно', 'что?',):
        {'^медленно&$не#давило#$создание&$дерево&$оно', '^медленно&$не#давит#$создание&$дерево&$оно',
         '^медленно&$не#будет_давить#$создание&$дерево&$оно', '^медленно&$не#раздавило#$создание&$дерево&$оно',
         '^медленно&$не#раздавит', '^медленно&$не#падало#$создание&$дерево&$оно',
         '^медленно&$не#падает#$создание&$дерево&$оно', '^медленно&$не#будет_падать#$создание&$дерево&$оно',
         '^медленно&$не#упало#$создание&$дерево&$оно', '^медленно&$не#упадёт#$создание&$дерево&$оно'},

    ('дерево#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'создание#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'оно#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи'):
        {'^медленно&$не#давило#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#давит#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#будет_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавило#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавит#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падало#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падает#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#будет_падать#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упало#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упадёт#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи'},

    ('как?#^коты&^камни&^они', 'куда?#^коты&^камни&^они', 'откуда?#^коты&^камни&^они', 'где?#^медленно',
     'когда?#^коты&^камни&^они', '$очень&^очень#медленно',
     '$очень&^очень#холодно',):
        {'^медленно&$не#давили#$коты&$камни&$они', '^медленно&$не#давят#$коты&$камни&$они',
         '^медленно&$не#будут_давить#$коты&$камни&$они', '^медленно&$не#раздавили#$коты&$камни&$они',
         '^медленно&$не#раздавят#$коты&$камни&$они', '^медленно&$не#падали#$коты&$камни&$они',
         '^медленно&$не#падают#$коты&$камни&$они', '^медленно&$не#будут_падать#$коты&$камни&$они',
         '^медленно&$не#упали#$коты&$камни&$они', '^медленно&$не#упадут#$коты&$камни&$они'},

    ('камни#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'коты#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
     'они#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',):
        {'^медленно&$не#давили#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#давят#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#будут_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавили#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#раздавят#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падали#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#падают#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#будут_падать#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упали#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         '^медленно&$не#упадут#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи'},

    ('как?#^медленно', 'где?#^медленно', 'куда?#^медленно', 'откуда?#^медленно', '$очень&^очень#медленно',):
        {'медленно', '$не#давить', '$не#раздавить', '$не#падать', '$не#упасть', 'написан#?$кот&$камень&$он',
         'написана#$девочка&$ветка&$она',
         'написано#$создание&$дерево&$оно', 'написаны#$коты&$камни&$они'},
    ('когда?', 'где?', 'как?', 'куда?', 'откуда?',):
        {'написан#?$кот&$камень&$он', 'написана#$девочка&$ветка&$она', 'написано#$создание&$дерево&$оно',
         'написаны#$коты&$камни&$они'},

    ('как?#^медленно', 'где?#^медленно', 'когда?#^медленно', 'куда?#^медленно', 'откуда?#^медленно',
     '^очень&$очень#медленно#^не', 'не',):
        {'^кот&^камень&^он#давил#$кот&$камень&$он', 'давила#$девочка&$ветка&$она', 'давило#$создание&$дерево&$оно',
         'давлю#$я', 'буду_давить#$я', '^кот&^камень&^он#раздавил#$кот&$камень&$он', 'раздавила#$девочка&$ветка&$она',
         'раздавило#$создание&$дерево&$оно', 'раздавлю#$я', 'давили#$коты&$камни&$они', 'давим#$мы', 'будем_давить#$мы',
         'раздавили#$коты&$камни&$они', 'раздавим#$мы', 'давишь#$ты', 'будешь_давить#$ты', 'раздавишь#$ты', 'дави#$ты',
         'раздави#$ты', 'давите#$вы', 'будете_давить#$вы', 'раздавите#$вы', 'давите*#$вы', 'раздавите*#$вы',
         '^кот&^камень&^он#падал#$кот&$камень&$он', 'падала#$девочка&$ветка&$она', 'падало#$создание&$дерево&$оно',
         'падаю#$я', 'буду_падать#$я', '^кот&^камень&^он#упал#$кот&$камень&$он', 'упала#$девочка&$ветка&$она',
         'упало#$создание&$дерево&$оно', 'упаду#$я', 'падали#$коты&$камни&$они', 'падаем#$мы', 'будем_падать#$мы',
         'упали#$коты&$камни&$они', 'упадём#$мы', 'падаешь#$ты', 'будешь_падать#$ты', 'упадёшь#$ты', 'падай#$ты',
         'упади#$ты', 'падаете#$вы', 'будете_падать#$вы', 'упадёте#$вы', 'падайте#$вы', 'упадите#$вы'},

    ('я#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',):
        {'давил#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'давила#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'давило#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'давлю#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'буду_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавил#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавила#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавило#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавлю#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'падал#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'падала#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'падало#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'падаю#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'буду_падать#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упал#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'упала#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упало#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'упаду#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи'},
    ('мы#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',):
        {'давили#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'давим#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'будем_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавили#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавим#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', },
    ('ты#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',):
        {'давил#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'давила#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'давило#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'давишь#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'будешь_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавил#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавила#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавило#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавишь#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'дави#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'раздави#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'падал#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'падала#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'падало#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'падаешь#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'будешь_падать#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упал#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'упала#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упало#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упадёшь#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'падай#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упади#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', },
    ('вы#^медленно&$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',):
        {'давили#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'давите#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'будете_давить#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавили#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавите#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'давите*#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'раздавите*#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'падали#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'падаете#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'будете_падать#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упали#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', 'упадёте#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'падайте#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи',
         'упадите#$пса&$кирпич&$девочку&$ветку&$собак&$кирпичи', },

    # nomn
    ('камень#^и&^,', 'кот#^и&^,', 'ветка#^и&^,', 'девочка#^и&^,', 'дерево#^и&^,', 'создание#^и&^,', 'камни#^и&^,',
     'коты#^и&^,'):
        {'камень', 'кот', 'ветка', 'девочка', 'дерево', 'создание', 'камни', 'коты'},

    ('какой?', 'который?', 'чей?', '$очень&^очень&^раздавил&$раздавил&^давил&^упал&$упал&^падал#синий',
     '$очень&^очень&^раздавил&$раздавил&^давил&^упал&$упал&^падал#падающий',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#падавший', '^раздавил&$раздавил&^давил&^упал&$упал&^падал#упавший',
     '$очень&^очень&^раздавил&$раздавил&^давил&^упал&$упал&^падал#рисующий',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#рисовавший',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#рисуемый',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#рисованный',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#написавший',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#написанный', 'рисуем', 'рисован', 'написан',
     '$очень&^очень&^раздавил&$раздавил&^давил&^упал&$упал&^падал#падающий',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#падавший',
     '^раздавил&$раздавил&^давил&^упал&$упал&^падал#упавший',):
        {'я#$раздавил', 'ты#$раздавил', 'он#$раздавил', 'кот#$раздавил', 'камень#$раздавил'},
    ('какая?', 'которая?', 'чья?', '$очень&^очень&^раздавила&$раздавила&^давила&^упала&$упала&^падала#синяя',
     '$очень&^очень&^раздавила&$раздавила&^давила&^упала&$упала&^падала#рисующая',
     '^раздавила&$раздавила&^давила&^упала&$упала&^падала#рисовавшая',
     '^раздавила&$раздавила&^давила&^упала&$упала&^падала#рисуемая',
     '^раздавила&$раздавила&^давила&^упала&$упала&^падала#рисованная',
     '^раздавила&$раздавила&^давила&^упала&$упала&^падала#написавшая',
     '^раздавила&$раздавила&^давила&^упала&$упала&^падала#написанная', 'рисуема', 'рисована', 'написана',
     '$очень&^очень&^раздавила&$раздавила&^давила&^упала&$упала&^падала#падающая',
     '^раздавила&$раздавила&^давила&^упала&$упала&^падала#падавшая',
     '^раздавила&$раздавила&^давила&^упала&$упала&^падала#упавшая',):
        {'я#$раздавила', 'ты#$раздавила', 'она#$раздавила', 'девочка#$раздавила', 'ветка#$раздавила'},
    ('какое?', 'которое?', 'чьё?', '$очень&^очень&^раздавило&$раздавило&^давило&^упало&$упало&^падало#красное',
     '$очень&^очень&^раздавило&$раздавило&^давило&^упало&$упало&^падало#рисующее',
     '^раздавило&$раздавило&^давило&^упало&$упало&^падало#рисовавшее',
     '^раздавило&$раздавило&^давило&^упало&$упало&^падало#рисуемое',
     '^раздавило&$раздавило&^давило&^упало&$упало&^падало#рисованное',
     '^раздавило&$раздавило&^давило&^упало&$упало&^падало#написавшее',
     '^раздавило&$раздавило&^давило&^упало&$упало&^падало#написанное', 'рисуемо', 'рисовано', 'написано',
     '$очень&^очень&^раздавило&$раздавило&^давило&^упало&$упало&^падало#падающее',
     '^раздавило&$раздавило&^давило&^упало&$упало&^падало#падавшее',
     '^раздавило&$раздавило&^давило&^упало&$упало&^падало#упавшее',):
        {'я#$раздавило', 'ты#$раздавило', 'оно#$раздавило', 'создание#$раздавило', 'дерево#$раздавило'},
    ('какие?', 'которые?', 'чьи?', '$очень&^очень&^раздавили&^давили&^упали&^падали#синие',
     '$очень&^очень&^раздавили&^давили&^упали&^падали#рисующие', '^раздавили&^давили&^упали&^падали#рисовавшие',
     '^раздавили&^давили&^упали&^падали#рисуемые', '^раздавили&^давили&^упали&^падали#рисованные',
     '^раздавили&^давили&^упали&^падали#написавшие', '^раздавили&^давили&^упали&^падали#написанные', 'рисуемы',
     'рисованы', 'написаны', '$очень&^очень&^раздавили&^давили&^упали&^падали#падающие',
     '^раздавили&^давили&^упали&^падали#падавшие', '^раздавили&^давили&^упали&^падали#упавшие',):
        {'мы#$раздавили', 'они#$раздавили', 'вы#$раздавили', 'коты#$раздавили', 'камни#$раздавили'},

    ('какой?#^кот&^камень', 'сколько?#^кот&^камень', 'который?#^кот&^камень', 'чей?#^кот&^камень',
     '$очень&^очень#синий#^кот&^камень&$кот&$камень',
     '$очень&^очень#рисующий#^кот&^камень&$кот&$камень', 'рисовавший#^кот&^камень&$кот&$камень',
     'рисуемый#^кот&^камень&$кот&$камень', 'рисованный#^кот&^камень&$кот&$камень',
     'написавший#^кот&^камень&$кот&$камень', 'написанный#^кот&^камень&$кот&$камень', 'рисуем', 'рисован', 'написан',
     '$очень&^очень#падающий#^кот&^камень&$кот&$камень', 'падавший#^кот&^камень&$кот&$камень',
     'упавший#^кот&^камень&$кот&$камень',):
        {'^когда?&^медленно&^не&$не#будет_давить', '^когда?&^медленно&^не&$не#давил', '^когда?&^медленно&^не&$не#давит',
         '^когда?&^медленно&^не&$не#раздавил', '^когда?&^медленно&^не&$не#раздавит',
         '^когда?&^медленно&^не&$не#будет_падать', '^когда?&^медленно&^не&$не#падал',
         '^когда?&^медленно&^не&$не#падает', '^когда?&^медленно&^не&$не#упал', '^когда?&^медленно&^не&$не#упадёт'},
    ('какая?#^девочка&^ветка', 'сколько?#^девочка&^ветка', 'которая?#^девочка&^ветка', 'чья?#^девочка&^ветка',
     '$очень&^очень#синяя#^девочка&^ветка&$девочка&$ветка',
     '$очень&^очень#рисующая#^девочка&^ветка&$девочка&$ветка', 'рисовавшая#^девочка&^ветка&$девочка&$ветка',
     'рисуемая#^девочка&^ветка&$девочка&$ветка', 'рисованная#^девочка&^ветка&$девочка&$ветка',
     'написавшая#^девочка&^ветка&$девочка&$ветка', 'написанная#^девочка&^ветка&$девочка&$ветка', 'рисуема', 'рисована',
     'написана', '$очень&^очень#падающая#^девочка&^ветка&$девочка&$ветка', 'падавшая#^девочка&^ветка&$девочка&$ветка',
     'упавшая#^девочка&^ветка&$девочка&$ветка',):
        {'^когда?&^медленно&^не&$не#давила', '^когда?&^медленно&^не&$не#давит',
         '^когда?&^медленно&^не&$не#будет_давить', '^когда?&^медленно&^не&$не#раздавила',
         '^когда?&^медленно&^не&$не#раздавит', '^когда?&^медленно&^не&$не#падала', '^когда?&^медленно&^не&$не#падает',
         '^когда?&^медленно&^не&$не#будет_падать', '^когда?&^медленно&^не&$не#упала',
         '^когда?&^медленно&^не&$не#упадёт'},
    ('какое?#^создание&^дерево', 'сколько?#^создание&^дерево', 'которое?#^создание&^дерево', 'чьё?#^создание&^дерево',
     '$очень&^очень#красное#^создание&^дерево&$создание&$дерево',
     '$очень&^очень#рисующее#^создание&^дерево&$создание&$дерево', 'рисовавшее#^создание&^дерево&$создание&$дерево',
     'рисуемое#^создание&^дерево&$создание&$дерево', 'рисованное#^создание&^дерево&$создание&$дерево',
     'написавшее#^создание&^дерево&$создание&$дерево', 'написанное#^создание&^дерево&$создание&$дерево', 'рисуемо',
     'рисовано', 'написано', '$очень&^очень#падающее#^создание&^дерево&$создание&$дерево',
     'падавшее#^создание&^дерево&$создание&$дерево', 'упавшее#^создание&^дерево&$создание&$дерево',):
        {'^когда?&^медленно&^не&$не#давило', '^когда?&^медленно&^не&$не#давит',
         '^когда?&^медленно&^не&$не#будет_давить', '^когда?&^медленно&^не&$не#раздавило',
         '^когда?&^медленно&^не&$не#раздавит', '^когда?&^медленно&^не&$не#падало', '^когда?&^медленно&^не&$не#падает',
         '^когда?&^медленно&^не&$не#будет_падать', '^когда?&^медленно&^не&$не#упало',
         '^когда?&^медленно&^не&$не#упадёт'},
    ('какие?#^коты&^камни', 'сколько?#^коты&^камни', 'которое?#^коты&^камни', 'чьё?#^коты&^камни',
     '$очень&^очень#синие#^коты&^камни&$коты&$камни',
     '$очень&^очень#рисующие#^коты&^камни&$коты&$камни', 'рисовавшие#^коты&^камни&$коты&$камни',
     'рисуемые#^коты&^камни&$коты&$камни', 'рисованные#^коты&^камни&$коты&$камни',
     'написавшие#^коты&^камни&$коты&$камни', 'написанные#^коты&^камни&$коты&$камни', 'рисуемы', 'рисованы', 'написаны',
     '$очень&^очень#падающие#^коты&^камни&$коты&$камни', 'падавшие#^коты&^камни&$коты&$камни',
     'упавшие#^коты&^камни&$коты&$камни',):
        {'^когда?&^медленно&^не&$не#давили', '^когда?&^медленно&^не&$не#давят',
         '^когда?&^медленно&^не&$не#будут_давить', '^когда?&^медленно&^не&$не#раздавили',
         '^когда?&^медленно&^не&$не#раздавят', '^когда?&^медленно&^не&$не#падали', '^когда?&^медленно&^не&$не#падают',
         '^когда?&^медленно&^не&$не#будут_падать', '^когда?&^медленно&^не&$не#упали',
         '^когда?&^медленно&^не&$не#упадут'},

    ('$очень&^очень#жёлт',):
        {'я#^раздавил&^упал', 'ты#^раздавил&^упал', 'он#^раздавил&^упал', 'кот#^раздавил&^упал',
         'камень#^раздавил&^упал'},
    ('$очень&^очень#желта',):
        {'я#^раздавила&^упала', 'ты#^раздавила&^упала', 'она#^раздавила&^упала', 'девочка#^раздавила&^упала',
         'ветка#^раздавила&^упала'},
    ('$очень&^очень#жёлто',):
        {'я#^раздавило&^упало', 'ты#^раздавило&^упало', 'оно#^раздавило&^упало', 'создание#^раздавило&^упало',
         'дерево#^раздавило&^упало'},
    ('$очень&^очень#жёлты',):
        {'мы#^раздавили&^упали', 'они#^раздавили&^упали', 'вы#^раздавили&^упали', 'коты#^раздавили&^упали',
         'камни#^раздавили&^упали'},

    ('светлее', 'как?', 'не',):
        {'я', 'ты', 'он', 'кот', 'камень', 'она', 'девочка', 'ветка', 'оно', 'создание', 'дерево', 'мы', 'они', 'вы',
         'коты', 'камни'},

    # gent
    ('без', 'нет',):
        {'меня', 'тебя', 'его', 'её', 'него', 'нас', 'их', 'вас'},
    ('кого?',):
        {'кота', 'девочки', 'создания', 'котов', 'меня', 'тебя', 'его', 'её', 'него', 'нас', 'их', 'вас'},
    ('чего?',):
        {'камня', 'ветки', 'дерева', 'камней'},
    ('скольких?',):
        {'нас', 'их', 'вас', 'котов', 'камней', },

    ('кота#^и&^,', 'камня#^и&^,', 'девочки#^и&^,', 'ветки#^и&^,', 'создания#^и&^,', 'дерева#^и&^,', 'котов#^и&^,',
     'камней#^и&^,'):
        {'кота', 'камня', 'девочки', 'ветки', 'создания', 'дерева', 'котов', 'камней'},

    ('камень', 'кот', 'ветка', 'девочка', 'дерево', 'создание', 'камни', 'коты', 'не', 'кота', 'камня', 'девочки',
     'ветки', 'создания', 'дерева', 'котов', 'камней', 'коту', 'камню', 'девочке', 'ветке', 'созданию', 'дереву',
     'котам', 'камням', 'кирпич', 'ветку', 'полено', 'кирпичи', 'пса', 'девочку', 'создание*', 'собак', 'котом',
     'девочкой', 'созданием', 'котами', 'камнем', 'веткой', 'деревом', 'камнями', 'коте', 'камне', 'собаке', 'палке',
     'создании**', 'дереве', 'котах', 'камнях', 'без', 'нет', 'светлее',):
        {'кота', 'камня', 'девочки', 'ветки', 'создания', 'дерева', 'котов', 'камней'},

    ('два',):
        {'кота', 'камня'},
    ('две',):
        {'девочки', 'ветки'},
    ('два**',):
        {'создания', 'дерева'},
    ('два*', 'четыре',):
        {'камня'},
    ('две*', 'четыре',):
        {'ветки'},
    ('два***', 'четыре',):
        {'дерева'},
    ('двух***', 'двух****', 'четырёх',):
        {'котов'},
    ('десять', 'двух', 'двух*', 'двух**', 'десяти', 'девять',):
        {'котов', 'камней'},

    ('^нет&^без#чьего?', '^нет&^без#которого?', '^нет&^без#какого?', '$очень&^очень&^нет&^без#синего',
     '$очень&^очень&^нет&^без#рисующего', '^нет&^без#рисовавшего',
     '^нет&^без#рисуемого', '^нет&^без#рисованного', '^нет&^без#написавшего', '^нет&^без#написанного',
     '$очень&^очень&^нет&^без#падающего', '^нет&^без#падавшего', '^нет&^без#упавшего',):
        {'^нет&^без#меня', '^нет&^без#тебя', '^нет&^без#его', '^нет&^без#кота', '^нет&^без#камня'},
    ('^нет&^без#чьей?', '^нет&^без#которой?', '^нет&^без#какой?*', '$очень&^очень&^нет&^без#синей',
     '$очень&^очень&^нет&^без#рисующей', '^нет&^без#рисовавшей', '^нет&^без#рисуемой',
     '^нет&^без#рисованной', '^нет&^без#написавшей', '^нет&^без#написанной', '$очень&^очень&^нет&^без#падающей',
     '^нет&^без#падавшей', '^нет&^без#упавшей',):
        {'^нет&^без#меня', '^нет&^без#тебя', '^нет&^без#её', '^нет&^без#девочки', '^нет&^без#ветки'},
    ('^нет&^без#чьего?*', '^нет&^без#которого?*', '^нет&^без#какого?*', '$очень&^очень&^нет&^без#красного',
     '$очень&^очень&^нет&^без#рисующего*', '^нет&^без#рисовавшего*',
     '^нет&^без#рисуемого*', '^нет&^без#рисованного*', '^нет&^без#написавшего*', '^нет&^без#написанного*',
     '$очень&^очень&^нет&^без#падающего*', '^нет&^без#падавшего*', '^нет&^без#упавшего*',):
        {'^нет&^без#меня', '^нет&^без#тебя', '^нет&^без#него', '^нет&^без#создания', '^нет&^без#дерева'},
    ('^нет&^без#чьих?', '^нет&^без#которых?', '^нет&^без#каких?*', '$очень&^очень&^нет&^без#синих',
     '$очень&^очень&^нет&^без#рисующих', '^нет&^без#рисовавших', '^нет&^без#рисуемых',
     '^нет&^без#рисованных', '^нет&^без#написавших', '^нет&^без#написанных', '$очень&^очень&^нет&^без#падающих',
     '^нет&^без#падавших', '^нет&^без#упавших',):
        {'^нет&^без#нас', '^нет&^без#их', '^нет&^без#вас', '^нет&^без#котов', '^нет&^без#камней'},

    # datv
    ('кому?',):
        {'мне', 'тебе', 'ему', 'коту', 'ей', 'девочке', 'нему',
         'созданию', 'нам', 'им', 'вам', 'котам'},
    ('чему?',):
        {'камню', 'ветке', 'дереву', 'камням'},
    ('скольким?',):
        {'нам', 'им', 'вам', 'котам', 'камням', },

    ('коту#^и&^,', 'камню#^и&^,', 'девочке#^и&^,', 'ветке#^и&^,', 'созданию#^и&^,', 'дереву#^и&^,', 'котам#^и&^,',
     'камням#^и&^,'):
        {'коту', 'камню', 'девочке', 'ветке', 'созданию', 'дереву', 'котам', 'камням'},

    ('кто?', 'что?', 'синий', 'синяя', 'синие', 'синие', 'камень', 'кот', 'ветка', 'девочка', 'дерево', 'создание',
     'камни', 'коты', 'я', 'ты', 'мы', 'вы', 'он', 'она', 'оно', 'они', 'некогда', 'медленно', 'без', 'давить',
     'раздавить', 'написав', 'давя', 'давив', 'не', 'будет_давить', 'давил', 'давит', 'раздавил', 'раздавит', 'давила',
     'раздавила', 'давило', 'раздавило', 'давили', 'давят', 'будут_давить', 'раздавили', 'раздавят', 'давлю',
     'буду_давить', 'раздавлю', 'давим', 'будем_давить', 'раздавим', 'давишь', 'будешь_давить', 'раздавишь', 'дави',
     'раздави', 'давите', 'будете_давить', 'раздавите', 'давите', 'раздавите',):
        {'мне', 'тебе', 'ему', 'коту', 'камню', 'ей', 'девочке', 'ветке', 'нему', 'созданию', 'дереву', 'нам', 'им',
         'вам', 'котам', 'камням'},

    ('двум', 'двум*', 'двум**', 'девяти',):
        {'котам', 'камням'},

    ('чьему?', 'которому?', 'какому?', '$очень&^очень#синему', 'рисующему', 'рисовавшему', 'рисуемому', 'рисованному',
     'написавшему', 'написанному',
     'падающему', 'падавшему', 'упавшему',):
        {'мне', 'тебе', 'ему', 'коту', 'камню'},
    ('чьей?*', 'которой?*', 'какой?**', '$очень&^очень#зелёной', 'рисующей*', 'рисовавшей*', 'рисуемой*', 'рисованной*',
     'написавшей*', 'написанной*',
     'падающей*', 'падавшей*', 'упавшей*',):
        {'мне', 'тебе', 'ей', 'девочке', 'ветке'},
    ('чьему?*', 'которому?*', 'какому?*', '$очень&^очень#красному', 'рисующему*', 'рисовавшему*', 'рисуемому*',
     'рисованному*', 'написавшему*', 'падающему*',
     'падавшему*', 'упавшему*', 'написанному*',):
        {'мне', 'тебе', 'нему', 'созданию', 'дереву'},
    ('чьим?', 'которым?', 'каким?', '$очень&^очень#синим', 'рисующим', 'рисовавшим', 'рисуемым', 'рисованным',
     'написавшим', 'написанным', 'падающим',
     'падавшим', 'упавшим',):
        {'нам', 'им', 'вам', 'котам', 'камням'},

    # accs
    ('кого?*',):
        {'меня*', 'тебя*', 'его*', 'пса', 'её*', 'девочку',
         'него*', 'создание*', 'нас*', 'вас*', 'их*', 'собак'},
    ('что?*',):
        {'кирпич', 'ветку', 'полено', 'кирпичи'},
    ('скольких?',):
        {'нас*', 'вас*', 'их*', 'собак', },
    ('сколько?*',):
        {'кирпичи', },

    ('кирпич#^и&^,', 'ветку#^и&^,', 'полено#^и&^,', 'кирпичи#^и&^,', 'пса#^и&^,', 'девочку#^и&^,', 'создание*#^и&^,',
     'собак#^и&^,'):
        {'кирпич', 'ветку', 'полено', 'кирпичи', 'пса', 'девочку', 'создание*', 'собак'},

    ('^на&^давлю&^падаю#чьего?**', '^на&^давлю&^падаю#которого?**', '^на&^давлю&^падаю#какого?**',
     '^на&^давлю&^падаю#зелёного', '^на&^давлю&^падаю#написавшего**#^на', '^на&^давлю&^падаю#написанного**#^на',
     '^на&^давлю&^падаю#рисующего**#^на', '^на&^давлю&^падаю#рисовавшего**#^на', '^на&^давлю&^падаю#рисуемого**#^на',
     '^на&^давлю&^падаю#рисованного**#^на', '^на&^давлю&^падаю#упавшего**#^на', '^на&^давлю&^падаю#падающего**#^на',
     '^на&^давлю&^падаю#падавшего**#^на',):
        {'меня*', 'тебя*', 'его*', 'пса'},
    ('^на&^давлю&^падаю#чей?*', '^на&^давлю&^падаю#который?*', '^на&^давлю&^падаю#какой?***',
     '^на&^давлю&^падаю#зелёный', '^на&^давлю&^падаю#написавший*#^на', '^на&^давлю&^падаю#написанный*#^на',
     '^на&^давлю&^падаю#рисующий*#^на', '^на&^давлю&^падаю#рисовавший*#^на', '^на&^давлю&^падаю#рисуемый*#^на',
     '^на&^давлю&^падаю#рисованный*#^на', '^на&^давлю&^падаю#упавший*#^на', '^на&^давлю&^падаю#падающий*#^на',
     '^на&^давлю&^падаю#падавший*#^на',):
        {'кирпич'},
    ('^на&^давлю&^падаю#чью?', '^на&^давлю&^падаю#которую?', '^на&^давлю&^падаю#какую?', '^на&^давлю&^падаю#зелёную',
     '^на&^давлю&^падаю#написавшую#^на', '^на&^давлю&^падаю#написанную#^на',
     '^на&^давлю&^падаю#рисующую#^на', '^на&^давлю&^падаю#рисовавшую#^на', '^на&^давлю&^падаю#рисуемую#^на',
     '^на&^давлю&^падаю#рисованную#^на', '^на&^давлю&^падаю#упавшую#^на', '^на&^давлю&^падаю#падающую#^на',
     '^на&^давлю&^падаю#падавшую#^на',):
        {'меня*', 'тебя*', 'её*', 'девочку', 'ветку'},
    ('^на&^давлю&^падаю#чьё?*', '^на&^давлю&^падаю#которое?*', '^на&^давлю&^падаю#какое?*', '^на&^давлю&^падаю#жёлтое',
     '^на&^давлю&^падаю#написавшее*#^на', '^на&^давлю&^падаю#написанное*#^на',
     '^на&^давлю&^падаю#рисующее*#^на', '^на&^давлю&^падаю#рисовавшее*#^на', '^на&^давлю&^падаю#рисуемое*#^на',
     '^на&^давлю&^падаю#рисованное*#^на', '^на&^давлю&^падаю#упавшее*#^на', '^на&^давлю&^падаю#падающее*#^на',
     '^на&^давлю&^падаю#падавшее*#^на',):
        {'меня*', 'тебя*', 'него*', 'создание*', 'полено'},
    (
        '^на&^давлю&^падаю#чьих?*', '^на&^давлю&^падаю#которых?*', '^на&^давлю&^падаю#каких?**',
        '^на&^давлю&^падаю#жёлтых',
        '^на&^давлю&^падаю#написавших*#^на', '^на&^давлю&^падаю#написанных*#^на',
        '^на&^давлю&^падаю#рисующих*#^на', '^на&^давлю&^падаю#рисовавших*#^на', '^на&^давлю&^падаю#рисуемых*#^на',
        '^на&^давлю&^падаю#рисованных*#^на', '^на&^давлю&^падаю#упавших*#^на', '^на&^давлю&^падаю#падающих*#^на',
        '^на&^давлю&^падаю#падавших*#^на',):
        {'нас*', 'вас*', 'их*', 'собак'},
    ('^на&^давлю&^падаю#чьи?*', '^на&^давлю&^падаю#которые?*', '^на&^давлю&^падаю#какие?*', '^на&^давлю&^падаю#жёлтые',
     '^на&^давлю&^падаю#написавшие*#^на', '^на&^давлю&^падаю#написанные*#^на',
     '^на&^давлю&^падаю#рисующие*#^на', '^на&^давлю&^падаю#рисовавшие*#^на', '^на&^давлю&^падаю#рисуемые*#^на',
     '^на&^давлю&^падаю#рисованные*#^на', '^на&^давлю&^падаю#упавшие*#^на', '^на&^давлю&^падаю#падающие*#^на',
     '^на&^давлю&^падаю#падавшие*#^на',):
        {'кирпичи'},

    ('давить#^на', 'раздавить#^на', 'написав#^на', 'давя#^на', 'давив#^на', 'не#^на', 'будет_давить#^на', 'давил#^на',
     'давит#^на', 'раздавил#^на', 'раздавит#^на', 'давила#^на', 'раздавила#^на', 'давило#^на', 'раздавило#^на',
     'давили#^на', 'давят#^на', 'будут_давить#^на', 'раздавили#^на', 'раздавят#^на', 'давлю#^на', 'буду_давить#^на',
     'раздавлю#^на', 'давим#^на', 'будем_давить#^на', 'раздавим#^на', 'давишь#^на', 'будешь_давить#^на',
     'раздавишь#^на', 'дави#^на', 'раздави#^на', 'давите#^на', 'будете_давить#^на', 'раздавите#^на', 'давите*#^на',
     'раздавите*#^на', 'падать#^на', 'упасть#^на', 'будет_падать#^на', 'падал#^на', 'падает#^на', 'упал#^на',
     'упадёт#^на', 'падала#^на', 'упала#^на', 'падало#^на', 'упало#^на', 'падали#^на', 'падают#^на',
     'будут_падать#^на', 'упали#^на', 'упадут#^на', 'падаю#^на', 'буду_падать#^на', 'упаду#^на', 'падаем#^на',
     'будем_падать#^на', 'упадём#^на', 'падаешь#^на', 'будешь_падать#^на', 'упадёшь#^на', 'падай#^на',
     'упади#^на', 'падаете#^на', 'будете_падать#^на', 'упадёте#^на', 'падайте#^на', 'упадите#^на', 'без',):
        {'^на#кирпич', '^на#ветку', '^на#полено', '^на#кирпичи', '^на#пса', '^на#девочку', '^на#создание*', '^на#собак',
         '^на#меня*', '^на#тебя*', '^на#его*', '^на#её*', '^на#него*', '^на#нас*', '^на#вас*', '^на#их*'},

    # ablt
    ('кем?',):
        {'мной', 'тобой', 'им*', 'котом', 'ей*', 'девочкой',
         'им**', 'созданием', 'нами', 'ими', 'вами', 'котами'},
    ('чем?',):
        {'камнем', 'веткой', 'деревом', 'камнями'},
    ('сколькими?',):
        {'нами', 'ими', 'вами', 'котами', 'камнями', },

    (
        'котом#^и&^,', 'девочкой#^и&^,', 'созданием#^и&^,', 'котами#^и&^,', 'камнем#^и&^,', 'веткой#^и&^,',
        'деревом#^и&^,',
        'камнями#^и&^,'):
        {'котом', 'девочкой', 'созданием', 'котами', 'камнем', 'веткой', 'деревом', 'камнями'},

    ('чьим?*', 'которым?*', 'каким?*', '$очень&^очень#синим*', 'написавшим*', 'написанным*', 'рисующим*', 'рисовавшим*',
     'рисуемым*', 'рисованным*',
     'упавшим*', 'падающим*', 'падавшим*',):
        {'мной', 'тобой', 'им*', 'котом', 'камнем'},
    ('чьей?**', 'которой?**', 'какой?****', '$очень&^очень#жёлтой', 'написавшей**', 'написанной**', 'рисующей**',
     'рисовавшей**', 'рисуемой**', 'рисованной**',
     'упавшей**', 'падающей**', 'падавшей**',):
        {'мной', 'тобой', 'ей*', 'девочкой', 'веткой'},
    ('чьим?**', 'которым?**', 'каким?**', '$очень&^очень#красным', 'написавшим**', 'написанным**', 'рисующим**',
     'рисовавшим**', 'рисуемым**',
     'рисованным**',
     'упавшим**', 'падающим**', 'падавшим**',):
        {'мной', 'тобой', 'им**', 'созданием', 'деревом'},
    ('чьими?', 'которыми?', 'какими?', '$очень&^очень#синими', 'написавшими', 'написанными', 'рисующими', 'рисовавшими',
     'рисуемыми', 'рисованными',
     'упавшими', 'падающими', 'падавшими',):
        {'нами', 'ими', 'вами', 'котами', 'камнями'},

    ('двумя#^синими', 'двумя*#^синими', 'двумя**#^синими', 'десятью#^синими',):
        {'котами', 'камнями'},

    ('падать#^с', 'упасть#^с', '^падать#не#^с', '^кот#будет_падать#^с', '^кот#падал#^с', '^кот#падает#^с',
     '^кот#упал#^с', '^ветка#упадёт#^с', '^ветка#падала#^с', '^ветка#упала#^с', '^дерево#падало#^с',
     '^дерево#упало#^с', '^коты#падали#^с', '^коты#падают#^с', '^коты#будут_падать#^с', '^коты#упали#^с',
     '^коты#упадут#^с', '^я#падаю#^с', '^я#буду_падать#^с', '^я#упаду#^с', '^мы#падаем#^с',
     '^мы#будем_падать#^с', '^мы#упадём#^с', '^ты#падаешь#^с', '^ты#будешь_падать#^с', '^ты#упадёшь#^с',
     '^ты#падай#^с', '^ты#упади#^с', '^вы#падаете#^с', '^вы#будете_падать#^с', '^вы#упадёте#^с',
     '^вы#падайте#^с', '^вы#упадите#^с', '^падал&^падать#камень', '^падал&^падать#кот', '^падала&^падать#ветка',
     '^падала&^падать#девочка', '^падало&^падать#дерево', '^падало&^падать#создание', '^падали&^падать#камни',
     '^падали&^падать#коты', 'давить#^с', 'раздавить#^с', 'написав#^с', 'давя#^с', 'давив#^с', '^давить#не#^с',
     '^кот#будет_давить#^с', '^кот#давил#^с', '^кот#давит#^с', '^кот#раздавил#^с', '^ветка#раздавит#^с',
     '^ветка#давила#^с', '^ветка#раздавила#^с', '^дерево#давило#^с', '^дерево#раздавило#^с', '^коты#давили#^с',
     '^коты#давят#^с', '^коты#будут_давить#^с', '^коты#раздавили#^с', '^коты#раздавят#^с', '^я#давлю#^с',
     '^я#буду_давить#^с', '^я#раздавлю#^с', '^мы#давим#^с', '^мы#будем_давить#^с', '^мы#раздавим#^с', '^ты#давишь#^с',
     '^ты#будешь_давить#^с', '^ты#раздавишь#^с', '^ты#дави#^с', '^ты#раздави#^с', '^вы#давите#^с',
     '^вы#будете_давить#^с', '^вы#раздавите#^с', '^вы#давите#^с', '^вы#раздавите#^с', '^давил&^давить#камень',
     '^давил&^давить#кот', '^давила&^давить#ветка', '^давила&^давить#девочка', '^давило&^давить#дерево',
     '^давило&^давить#создание', '^давили&^давить#камни', '^давили&^давить#коты', 'без',):
        {'^с#котом', '^с#девочкой', '^с#созданием', '^с#котами', '^с#камнем', '^с#веткой', '^с#деревом', '^с#камнями',
         '^с#мной', '^с#тобой', '^с#им*', '^с#ей*', '^с#им**', '^с#нами', '^с#ими', '^с#вами'},

    # loct
    ('^о#ком?',):
        {'^о#мне**', '^о#тебе**', '^о#нём', '^о#коте', '^о#ней', '^о#собаке',
         '^о#нём*', '^о#создании**', '^о#нас**', '^о#них', '^о#вас**', '^о#котах'},
    ('^о#чём?',):
        {'^о#камне', '^о#палке', '^о#дереве', '^о#камнях'},
    ('^о#скольких?**',):
        {'^о#нас**', '^о#них', '^о#вас**', '^о#котах', '^о#камнях', },

    ('коте#^и&^,', 'камне#^и&^,', 'собаке#^и&^,', 'палке#^и&^,', 'создании**#^и&^,', 'дереве#^и&^,', 'котах#^и&^,',
     'камнях#^и&^,'):
        {'коте', 'камне', 'собаке', 'палке', 'создании**', 'дереве', 'котах', 'камнях'},

    ('^о#каком?', '^о#котором?', '^о#чьём?', '^о&$очень&^очень#синем', '^о#написавшем', '^о#написанном', '^о#рисующем',
     '^о#рисовавшем', '$о#рисуемом',
     '^о#рисованном', '^о#упавшем', '^о#падающем', '^о#падавшем',):
        {'^о&$о#мне**', '^о&$о#тебе**', '^о&$о#нём', '^о&$о#коте', '^о&$о#камне'},
    (
        '^о#чьей?***', '^о#которой?***', '^о#какой?*****', '^о&$очень&^очень#белой', '^о#написавшей***',
        '^о#написанной***',
        '^о#рисующей***', '^о#рисовавшей***',
        '^о#рисуемой***', '^о#рисованной***', '^о#упавшей***', '^о#падающей***', '^о#падавшей***',):
        {'^о&$о#мне**', '^о&$о#тебе**', '^о&$о#ней', '^о&$о#собаке', '^о&$о#палке'},
    ('^о#чьём?*', '^о#котором?*', '^о#каком?*', '^о&$очень&^очень#красном', '^о#написавшем*', '^о#написанном*',
     '^о#рисующем*', '^о#рисовавшем*', '^о#рисуемом*',
     '^о#рисованном*', '^о#упавшем*', '^о#падающем*', '^о#падавшем*',):
        {'^о&$о#мне**', '^о&$о#тебе**', '^о&$о#нём*', '^о&$о#создании**', '^о&$о#дереве'},
    ('^о#чьих?**', '^о#которых?**', '^о#каких?', '^о&$очень&^очень#красных', '^о#написавших**', '^о#написанных**',
     '^о#рисующих**', '^о#рисовавших**',
     '^о#рисуемых**', '^о#рисованных**', '^о#упавших**', '^о#падающих**', '^о#падавших**',):
        {'^о&$о#нас**', '^о&$о#них', '^о&$о#вас**', '^о&$о#котах', '^о&$о#камнях'},

    ('^о#двух*****', '^о#двух******', '^о#двух*******', '^о#восьми',):
        {'$о#котах', '$о#камнях'},

    ('падать#^на&$упал', 'упасть#^на&$кот', 'упав#^на&$коту', 'падая#^на&$ветку', 'падав#^на&$камень',
     'написав#^на&$коту', 'давя#^на&$ветку', 'давив#^на&$камень', 'не#^на&$давя', 'будет_падать#^на&$ветку',
     'падал#^на&$медленно', 'падает#^на&$медленно', 'упал#^на&$медленно', 'упадёт#^на&$медленно',
     'падала#^на&$медленно', 'упала#^на&$медленно', 'падало#^на&$создание*', 'упало#^на&$медленно',
     'падали#^на&$коты', 'падают#^на&$коты', 'будут_падать#^на&$коты', 'упали#^на&$медленно', 'упадут#^на&$камни',
     'падаю#^на&$я', 'буду_падать#^на&$я', 'упаду#^на&$я', 'падаем#^на&$мы', 'будем_падать#^на&$мы',
     'упадём#^на&$мы', 'падаешь#^на&$ты', 'будешь_падать#^на&$ты', 'упадёшь#^на&$ты', 'падай#^на&$ты',
     'упади#^на&$ты', 'падаете#^на&$вы', 'будете_падать#^на&$вы', 'упадёте#^на&$вы', 'падайте#^на&$вы',
     'упадите#^на&$вы', 'камень#^на&$падал', 'кот#^на&$падал', 'ветка#^на&$падала', 'девочка#^на&$падала',
     'дерево#^на&$падало', 'создание#^на&$падало', 'камни#^на&$падали', 'коты#^на&$падал', 'давить#^на&$раздавил',
     'раздавить#^на&$кот', 'написав#^на&$коту', 'давя#^на&$ветку', 'давив#^на&$камень', 'не#^на&$давя',
     'будет_давить#^на&$ветку', 'давил#^на&$медленно', 'давит#^на&$медленно', 'раздавил#^на&$медленно',
     'раздавит#^на&$медленно', 'давила#^на&$медленно', 'раздавила#^на&$медленно', 'давило#^на&$создание*',
     'раздавило#^на&$медленно', 'давили#^на&$коты', 'давят#^на&$коты', 'будут_давить#^на&$коты',
     'раздавили#^на&$медленно', 'раздавят#^на&$камни', 'давлю#^на&$я', 'буду_давить#^на&$я', 'раздавлю#^на&$я',
     'давим#^на&$мы', 'будем_давить#^на&$мы', 'раздавим#^на&$мы', 'давишь#^на&$ты', 'будешь_давить#^на&$ты',
     'раздавишь#^на&$ты', 'дави#^на&$ты', 'раздави#^на&$ты', 'давите#^на&$вы', 'будете_давить#^на&$вы',
     'раздавите#^на&$вы', 'давите#^на&$вы', 'раздавите#^на&$вы', 'камень#^на&$давил', 'кот#^на&$давил',
     'ветка#^на&$давила', 'девочка#^на&$давила', 'дерево#^на&$давило', 'создание#^на&$давило', 'камни#^на&$давили',
     'коты#^на&$давил', 'без#$котов',):
        {'^о#коте', '^о#камне', '^о#собаке', '^о#палке', '^о#создании**', '^о#дереве', '^о#котах', '^о#камнях',
         '^о#мне**', '^о#тебе**', '^о#нём', '^о#ней', '^о#нём*', '^о#нас**', '^о#них', '^о#вас**'},

    # adjf
    ('$очень&^очень#медленно', 'не',):
        {'синий', 'рисующий#$кот&$камень&$он&$кота&$камень&$он', 'рисовавший', 'рисуемый', 'рисованный', 'написавший',
         'написанный', 'синяя', 'рисующая', 'рисовавшая', 'рисуемая', 'рисованная', 'написавшая', 'написанная',
         'красное', 'рисующее', 'рисовавшее', 'рисуемое', 'рисованное', 'написавшее', 'написанное', 'синие', 'рисующие',
         'рисовавшие', 'рисуемые', 'рисованные', 'написавшие', 'написанные', 'синего', 'рисующего', 'рисовавшего',
         'рисуемого', 'рисованного', 'написавшего', 'написанного', 'синей', 'рисующей', 'рисовавшей', 'рисуемой',
         'рисованной', 'написавшей', 'написанной', 'красного', 'рисующего*', 'рисовавшего*', 'рисуемого*',
         'рисованного*', 'написавшего*', 'написанного*', 'синих', 'рисующих', 'рисовавших', 'рисуемых', 'рисованных',
         'написавших', 'написанных', 'синему', 'рисующему', 'рисовавшему', 'рисуемому', 'рисованному', 'написавшему',
         'написанному', 'зелёной', 'рисующей*', 'рисовавшей*', 'рисуемой*', 'рисованной*', 'написавшей*', 'написанной*',
         'красному', 'рисующему*', 'рисовавшему*', 'рисуемому*', 'рисованному*', 'написавшему*', 'написанному*',
         'синим', 'рисующим', 'рисовавшим', 'рисуемым', 'рисованным', 'написавшим', 'написанным', 'зелёного', 'зелёный',
         'зелёную', 'жёлтое', 'жёлтых', 'жёлтые', 'синим*', 'жёлтой', 'красным', 'синими', 'синем', 'белой', 'красном',
         'красных', 'написавшие*', 'написанные*', 'рисующие*', 'рисовавшие*', 'рисуемые*', 'рисованные*', 'написавших*',
         'написанных*', 'рисующих*', 'рисовавших*', 'рисуемых*', 'рисованных*', 'написавшее*', 'написанное*',
         'рисующее*', 'рисовавшее*', 'рисуемое*', 'рисованное*', 'написавшую', 'написанную', 'рисующую', 'рисовавшую',
         'рисуемую', 'рисованную', 'написавшего**', 'написанного**', 'рисующего**', 'рисовавшего**', 'рисуемого**',
         'рисованного**', 'написавший*', 'написанный*', 'рисующий*', 'рисовавший*', 'рисуемый*', 'рисованный*',
         'написавших**', 'написанных**', 'рисующих**', 'рисовавших**', 'рисуемых**', 'рисованных**', 'написавшем*',
         'написанном*', 'рисующем*', 'рисовавшем*', 'рисуемом*', 'рисованном*', 'написавшей***', 'написанной***',
         'рисующей***', 'рисовавшей**', 'рисуемой***', 'рисованной***', 'написавшем', 'написанном', 'рисующем',
         'рисовавшем', 'рисуемом', 'рисованном', 'написавшими', 'написанными', 'рисующими', 'рисовавшими', 'рисуемыми',
         'рисованными', 'написавшим**', 'написанным**', 'рисующим**', 'рисовавшим**', 'рисуемым**', 'рисованным**',
         'написавшей**', 'написанной**', 'рисующей**', 'рисовавшей***', 'рисуемой**', 'рисованной**', 'написавшим*',
         'написанным*', 'рисующим*', 'рисовавшим*', 'рисуемым*', 'рисованным*', 'написав', 'давя', 'давив', 'рисуем',
         'рисуема', 'рисуемо', 'рисуемы', 'рисован', 'рисована', 'рисовано', 'рисованы', 'написан', 'написана',
         'написано', 'написаны', 'написав', 'падающий#^кот&^камень&^он&^кота&^камень&^он', 'падавший', 'упавший',
         'падающая', 'падавшая', 'упавшая', 'падающее', 'падавшее', 'упавшее', 'падающие', 'падавшие', 'упавшие',
         'падающего', 'падавшего', 'упавшего', 'падающей', 'падавшей', 'упавшей', 'падающего*', 'падавшего*',
         'упавшего*', 'падающих', 'падавших', 'упавших', 'падающему', 'падавшему', 'упавшему', 'падающей*', 'падавшей*',
         'упавшей*', 'падающему*', 'падавшему*', 'упавшему*', 'падающим', 'падавшим', 'упавшим', 'упавшие*',
         'падающие*', 'падавшие*', 'упавших*', 'падающих*', 'падавших*', 'упавшее*', 'падающее*', 'падавшее*',
         'упавшую', 'падающую', 'падавшую', 'упавшего**', 'падающего**', 'падавшего**', 'упавший*', 'падающий*',
         'падавший*', 'упавших**', 'падающих**', 'падавших**', 'упавшем*', 'падающем*', 'падавшем*', 'упавшей***',
         'падающей***', 'падавшей**', 'упавшем', 'падающем', 'падавшем', 'упавшими', 'падающими', 'падавшими',
         'упавшим**', 'падающим**', 'падавшим**', 'упавшей**', 'падающей**', 'упав', 'падавшей***', 'упавшим*',
         'падающим*', 'падавшим*', 'упав', 'падая', 'падав'},

}

rules = defaultdict(set)
for k, v in _rules.items():
    for k_word in k:
        for v_word in v:
            rules[k_word].add(v_word)
            rules[v_word].add(k_word)
