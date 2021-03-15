import requests
import re

def yesNo():
  option = ''
  options = {'да': True, 'нет': False}
  while option not in options:
    print('Выберите: {}/{}'.format(*options))
    option = input().lower()
  return options[option]

def step1():
    print(
        'Утка-маляр решила погулять. '
        'Взять ей зонтик? ☂ '
    )
    if yesNo():
        return step2_umbrella()
    return step2_no_umbrella()

def step2_umbrella(counter = 0):
    print(
        'Ты ' + counter * 'точно ' + 'уверен?'
    )
    counter+=1
    if yesNo():
        return step2_umbrella(counter)
    return step1()

def step2_no_umbrella():
    print(
        'Правильно, это же утка. Она гидрофобная. \n'
        'Да и как ей зонтик держать вообще? У неё же лапки.\n'
        'А тебе интересно, почему утка маляр вообще?'
    )
    if yesNo():
        return step3_interesting(True)
    return step3_interesting(False)
    
def step3_interesting(interest):
    if interest:
        print(
            'Мне тоже интересно, но я не знаю.\n'
            'Такую домашку дали по питону.'
        )
    else:
        print('Ну и правильно. Любопытной Варваре на базаре нос оторвали.')
        
    print(
        'Может, анекдот? А то хз какие ещё шаги делать дальше'
    )
    if yesNo():
        return step4_joke()
    return step4_no_jokes()
    
def step4_joke():
    req = requests.get("http://rzhunemogu.ru/Rand.aspx?CType=1")
    if req.status_code != 200:
        print(
            'Сорян, анекдота не будет. Что-то с сетью или апишка тупит. '
            'Я честно пытался :с\n'
            'Понравилась прога?'
        )
        if yesNo():
            return step5_like()
        return step5_dislike()
        # Знаю, что предыдущие три строки можно было вынести в конец метода 
        # и поставить здесь else, но хотелось показать плоский код
    joke = re.search(r'<content>(.*)</content>', req.text.replace('\r\n', ' '))
    print(joke.group(0)[9:-10])
    print('\nЕщё шутеечку?')
    if yesNo():
        return step4_joke()
    print('А вообще смешно было?')
    if yesNo():
        return step5_like()
    return step5_dislike()

def step4_no_jokes():
    print(
        'Ну раз мы такие серьёзные, то, может, '
        'бренди бокальчик? Испанский, у друга производство своё!'
    )
    if yesNo():
        return step5_like()
    return step5_dislike()
    
def step5_like():
    print('Тогда надеюсь на отличную оценку ;)')

def step5_dislike():
    print('Обида. Пойду JS учить тогда!')
if __name__ == '__main__':
  step1()
  print(
    'Автор программы - Аникеев Г.Л. - не имел цели оскорбить кого-либо. '
    'Всё сказанное выше является шуткой и не должно быть воспринято всерьёз. '
    'Мир, труд, котики (или пёсики/крыски/мухи, кому что нравится)!'
  )