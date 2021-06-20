import pytest
import main


def test_long_executing_task():
    pass  # ???


def test_potentially_unsafe_func_ok():
    result = main.potentially_unsafe_func('name')
    assert result == 'test'


def test_potentially_unsafe_func_supresses():
    result = main.potentially_unsafe_func('helloworld')
    assert result == None


def test_sum_of_values_ok():
    result = main.sum_of_values((1, 2))
    assert result == 3


def test_sum_of_values_exception():
    with pytest.raises(ValueError):
        main.sum_of_values((1, 3, 5, 9))


def test_show_message_ok():
    main.show_message('Howdy, howdy my little friend')


def test_show_message_exception():
    with pytest.raises(ValueError):
        main.show_message('Howdy')


def test_process_text_ok():
    result = main.process_text('the French'
                               ' revolution resulted in 3 concepts: '
                               'freedom,equality,fraternity')
    assert result == "ThE FrencH RevolutioN ResulteD IN 33 Concepts, Freedom equality fraternitY"


def test_process_text_ok_2():
    result = main.another_process('the French '
                                  'revolution resulted in 3 concepts: '
                                  'freedom,equality,fraternity')
    assert result == "ThE FrencH RevolutioN ResulteD IN 33 Concepts, FreedoM EqualitY FraternitY"
