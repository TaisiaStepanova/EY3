from lub import *


class Controller:
    def __init__(self):
        super().__init__()

    def setView(self, view):
        self.view = view

    def get_data(self):
        dict2 = read_dict()
        dict = []
        for i in dict2:
            dict.append(i['word'])
        return dict

    def search_data(self, filter):
        data = find_in_main_dict(read_dict(), filter)
        if data == None:
            return []
        return [data['word']]

    def del_word(self, word):
        new_dict = remove_from_main_dict(read_dict(), str(word.id))
        save_dict(new_dict)
        self.view.show_data('nan')

    def selected(self, filename, label, button):
        if filename[0].find('docx', -4) == -1:
            label.text = 'Выберите docs файл!'
            button.disabled = True
        else:
            label.text = ''
            self.file = filename[0]
            button.disabled = False

    def load_word(self, label, button=None):
        new_dict = analize(read_dict(), self.file)
        save_dict(new_dict)
        button.disabled = True
        label.text = 'Загружено'
        self.view.show_data('nan')

    def get_forms(self, filter):
        data = find_in_main_dict(read_dict(), filter)
        data_tmp = []
        for i in data:
            if i != "word":
                for j in data[i]:
                    data_tmp.append([i, j])
        if data == None:
            return []
        return data_tmp

    def edit_form(self, new_form, label):
        dict = read_dict()
        new_dict = change_word_dict(dict, self.view.word, self.view.form, new_form.text)
        save_dict(new_dict)
        label.text = 'Изменено'
        self.view.show_data_form(self.view.word)
