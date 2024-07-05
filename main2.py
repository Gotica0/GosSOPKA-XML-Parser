from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re

from lxml import etree


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def click():
    window = Tk()
    window.title("Новое окно")
    window.geometry("250x200")


def clickx():
    window = Tk()
    window.title("Новое окно")
    window.geometry("500x200")


def selected1(event):
    # получаем выделенный элемент
    selection = combobox1.get()
    print(selection)
    SvCentrGS.set("КлассЦентр", selection)


def selected2(event):
    # получаем выделенный элемент
    selection = combobox2.get()
    print(selection)
    SvCentrGS.set("СхемВерс", selection)


def generate_xml():
    # dom = md.parseString(etree.tostring(SvCentrGS, encoding='unicode'))
    # pretty_xml_str = dom.toprettyxml(indent="  ")
    # print(pretty_xml_str)
    global inn_for_xml
    global entry1000
    global entry2000

    SvCentrGS.set("ДатаФорм", entry1000.get())
    SvCentrGS.set("НаимЦентр", entry2000.get())

    print(etree.tostring(SvCentrGS, pretty_print=True, encoding='unicode'))
    tree1 = etree.ElementTree(SvCentrGS)

    # Запись дерева в файл
    with open(inn_for_xml + "-" + entry1000.get() + "-v-00-0.xml", "wb") as f:
        tree1.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)


def save_data_svul(string, int, ogrn_value, inn_value, kpp_value, naim_poln, naim_sokr, tip, site, okved, okogu, okopf):
    # Проверка введенных данных
    pattern_ORGN = r'^[0-9]{13}$'
    pattern_INN = r'^([0-9][1-9]|[1-9][0-9])[0-9]{8}$'
    pattern_KPP = r'^([0-9][1-9]|[1-9][0-9])([0-9]{2})([0-9A-F]{2})([0-9]{3})$'
    pattern_uri = r'^[a-zA-Z][a-zA-Z0-9+.-]*:([^/\s]+(/[^/\s]*)*)?$'
    patterns_okved = [
        r'^[0-9]{2}$',  # Два числа
        r'^[0-9]{2}\.[0-9]$',  # Два числа, точка, одно число
        r'^[0-9]{2}\.[0-9]{2}$',  # Два числа, точка, два числа
        r'^[0-9]{2}\.[0-9]{2}\.[0-9]$',  # Два числа, точка, два числа, точка, одно число
        r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$',  # Два числа, точка, два числа, точка, два числа
    ]

    if not re.match(pattern_ORGN, ogrn_value):
        messagebox.showerror("Ошибка", "Введите корректный ОГРН (13 цифр)")
        return
    if not re.match(pattern_INN, inn_value):
        messagebox.showerror("Ошибка", "Введите корректный ИНН (10 цифр)")
        return
    if not re.match(pattern_KPP, kpp_value):
        messagebox.showerror("Ошибка", "Введите корректный КПП (9 символов)")
        return
    if not (1 <= len(naim_poln) <= 1000):
        messagebox.showerror("Ошибка",
                             "Введите корректный НаимЮЛПолн (минимальная - 1 символ, максимальная - 1000 символов)")
        return
    if not (0 <= len(naim_sokr) <= 510):
        messagebox.showerror("Ошибка",
                             "Введите корректный НаимЮЛСокр (минимальная - 0 символ, максимальная - 1000 символов)")
        return
    valid_okved = False
    for pattern in patterns_okved:
        if re.match(pattern, okved):
            valid_okved = True
            break
    if not valid_okved:
        messagebox.showerror("Ошибка", "Введите корректный ОКВЭД")
        return
    if not re.match(r'^[0-9]{7}$', okogu) and len(okogu) > 0:
        messagebox.showerror("Ошибка", "Введите корректный ОКОГУ (7 цифр)")
        return
    if not re.match(r'^[0-9]{5}$', okopf) and len(okopf) > 0:
        messagebox.showerror("Ошибка", "Введите корректный ОКОПФ (5 цифр)")
        return

    global inn_for_xml
    inn_for_xml = inn_value
    global SvUL_window
    SvUL_window.destroy()
    save_data_svul_2(string, int, ogrn_value, inn_value, kpp_value, naim_poln, naim_sokr, tip, site, okved, okogu,
                     okopf)


def SvUL_button_clicked(string, int):
    global SvUL_window
    SvUL_window = Tk()
    SvUL_window.title(string)
    SvUL_window.geometry("900x600")

    label0_SvUL = ttk.Label(SvUL_window, text='ОРГН')
    label0_SvUL.grid(row=0, column=0, padx=5, pady=5)
    CreateToolTip(label0_SvUL, text='Основной государственный регистрационный номер юридического лица')
    entry0_SvUL = ttk.Entry(SvUL_window, width=50)
    entry0_SvUL.grid(row=0, column=1, padx=5, pady=5)

    label1_SvUL = ttk.Label(SvUL_window, text='ИНН')
    label1_SvUL.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(label1_SvUL, text='Идентификационный номер налогоплательщика юридического лица')
    entry1001 = ttk.Entry(SvUL_window, width=50)
    entry1001.grid(row=1, column=1, padx=5, pady=5)

    label2_SvUL = ttk.Label(SvUL_window, text='КПП')
    label2_SvUL.grid(row=2, column=0, padx=5, pady=5)
    CreateToolTip(label2_SvUL, text='Код причины постановки на учет юридического лица')
    entry2_SvUL = ttk.Entry(SvUL_window, width=50)
    entry2_SvUL.grid(row=2, column=1, padx=5, pady=5)

    label3_SvUL = ttk.Label(SvUL_window, text='НаимЮЛПолн')
    label3_SvUL.grid(row=3, column=0, padx=5, pady=5)
    CreateToolTip(label3_SvUL, text='Полное наименование юридического лица')
    entry3_SvUL = ttk.Entry(SvUL_window, width=50)
    entry3_SvUL.grid(row=3, column=1, padx=5, pady=5)

    label4_SvUL = ttk.Label(SvUL_window, text='НаимЮЛСокр*')
    label4_SvUL.grid(row=4, column=0, padx=5, pady=5)
    CreateToolTip(label4_SvUL, text='Сокращенное наименование юридического лица')
    entry4_SvUL = ttk.Entry(SvUL_window, width=50)
    entry4_SvUL.grid(row=4, column=1, padx=5, pady=5)

    tip_ul = ['ФЕДЕРАЛЬНЫЙ ОРГАН ГОСУДАРСТВЕННОЙ ВЛАСТИ', 'РЕГИОНАЛЬНЫЙ ОРГАН ГОСУДАРСТВЕННОЙ ВЛАСТИ',
              'ЦЕНТРАЛЬНЫЙ БАНК РОССИЙСКОЙ ФЕДЕРАЦИИ', 'НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ', 'КОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ',
              'МЕСТНОЕ САМОУПРАВЛЕНИЕ']
    label5_SvUL = ttk.Label(SvUL_window, text='Тип')
    label5_SvUL.grid(row=5, column=0, padx=5, pady=5)
    CreateToolTip(label5_SvUL, text='Тип юридического лица')
    combobox5_SvUL = ttk.Combobox(SvUL_window, values=tip_ul, state='readonly', width=50)
    combobox5_SvUL.grid(row=5, column=1, padx=5, pady=5)

    label6_SvUL = ttk.Label(SvUL_window, text='Сайт*')
    label6_SvUL.grid(row=6, column=0, padx=5, pady=5)
    CreateToolTip(label6_SvUL, text='Официальный сайт юридического лица')
    entry6_SvUL = ttk.Entry(SvUL_window, width=50)
    entry6_SvUL.grid(row=6, column=1, padx=5, pady=5)

    label7_SvUL = ttk.Label(SvUL_window, text='ОКВЭД')
    label7_SvUL.grid(row=7, column=0, padx=5, pady=5)
    CreateToolTip(label7_SvUL, text='Код из Общероссийского классификатора видов экономической деятельности')
    entry7_SvUL = ttk.Entry(SvUL_window, width=50)
    entry7_SvUL.grid(row=7, column=1, padx=5, pady=5)

    label8_SvUL = ttk.Label(SvUL_window, text='ОКОГУ*')
    label8_SvUL.grid(row=8, column=0, padx=5, pady=5)
    CreateToolTip(label8_SvUL, text='Общероссийский классификатор органов государственной власти и управления')
    entry8_SvUL = ttk.Entry(SvUL_window, width=50)
    entry8_SvUL.grid(row=8, column=1, padx=5, pady=5)

    label9_SvUL = ttk.Label(SvUL_window, text='ОКОПФ*')
    label9_SvUL.grid(row=9, column=0, padx=5, pady=5)
    CreateToolTip(label9_SvUL, text='Общероссийский классификатор организационно-правовых форм')
    entry9_SvUL = ttk.Entry(SvUL_window, width=50)
    entry9_SvUL.grid(row=9, column=1, padx=5, pady=5)

    label10_SvUL = ttk.Label(SvUL_window, text='* - необязательные данные')
    label10_SvUL.grid(row=11, column=0, padx=5, pady=5)

    btn1_SvUL = ttk.Button(SvUL_window, text="Сохранить данные",
                           command=lambda: save_data_svul(string, int, entry0_SvUL.get(), entry1001.get(),
                                                          entry2_SvUL.get(),
                                                          entry3_SvUL.get(), entry4_SvUL.get(), combobox5_SvUL.get(),
                                                          entry6_SvUL.get(), entry7_SvUL.get(), entry8_SvUL.get(),
                                                          entry9_SvUL.get()))
    btn1_SvUL.grid(row=12, column=1, padx=5, pady=5)


def save_data_svcenteradr(kod_reg, naim_reg, index, naim_gor, adres):
    # Проверка введенных данных
    pattern_ORGN = r'^[0-9]{13}$'
    pattern_INN = r'^([0-9][1-9]|[1-9][0-9])[0-9]{8}$'
    pattern_KPP = r'^([0-9][1-9]|[1-9][0-9])([0-9]{2})([0-9A-F]{2})([0-9]{3})$'
    pattern_uri = r'^[a-zA-Z][a-zA-Z0-9+.-]*:([^/\s]+(/[^/\s]*)*)?$'
    patterns_okved = [
        r'^[0-9]{2}$',  # Два числа
        r'^[0-9]{2}\.[0-9]$',  # Два числа, точка, одно число
        r'^[0-9]{2}\.[0-9]{2}$',  # Два числа, точка, два числа
        r'^[0-9]{2}\.[0-9]{2}\.[0-9]$',  # Два числа, точка, два числа, точка, одно число
        r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$',  # Два числа, точка, два числа, точка, два числа
    ]

    CodRegion.text = kod_reg
    NaimRegion.text = naim_reg
    if len(index) > 0:
        Indeks.text = index
    else:
        SvCentrAdr.remove(Indeks)
    if len(naim_gor) > 0:
        NaimGor.text = naim_gor
    else:
        SvCentrAdr.remove(NaimGor)
    Adres.text = adres

    # print(etree.tostring(SvCentrAdr, encoding='unicode', method='xml'))
    # Если валидация прошла успешно, сохраняем данные
    # save_data_to_xml(ogrn_value, inn_value)
    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global SvCenterAdr_window
    SvCenterAdr_window.destroy()


def SvCenterAdr_button_clicked(string):
    global SvCenterAdr_window
    SvCenterAdr_window = Tk()
    SvCenterAdr_window.title(string)
    SvCenterAdr_window.geometry("900x600")

    label0_SvCenterAdr = ttk.Label(SvCenterAdr_window, text='КодРегион')
    label0_SvCenterAdr.grid(row=0, column=0, padx=5, pady=5)
    CreateToolTip(label0_SvCenterAdr, text='Код субъекта Российской Федерации')
    entry0_SvCenterAdr = ttk.Entry(SvCenterAdr_window, width=50)
    entry0_SvCenterAdr.grid(row=0, column=1, padx=5, pady=5)

    label1_SvCenterAdr = ttk.Label(SvCenterAdr_window, text='НаимРегион')
    label1_SvCenterAdr.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(label1_SvCenterAdr, text='Наименование субъекта Российской Федерации')
    entry1_SvCenterAdr = ttk.Entry(SvCenterAdr_window, width=50)
    entry1_SvCenterAdr.grid(row=1, column=1, padx=5, pady=5)

    label2_SvCenterAdr = ttk.Label(SvCenterAdr_window, text='Индекс*')
    label2_SvCenterAdr.grid(row=2, column=0, padx=5, pady=5)
    CreateToolTip(label2_SvCenterAdr, text='Почтовый индекс')
    entry2_SvCenterAdr = ttk.Entry(SvCenterAdr_window, width=50)
    entry2_SvCenterAdr.grid(row=2, column=1, padx=5, pady=5)

    label3_SvCenterAdr = ttk.Label(SvCenterAdr_window, text='НаимГор*')
    label3_SvCenterAdr.grid(row=3, column=0, padx=5, pady=5)
    CreateToolTip(label3_SvCenterAdr, text='Наименование населенного пункта')
    entry3_SvCenterAdr = ttk.Entry(SvCenterAdr_window, width=50)
    entry3_SvCenterAdr.grid(row=3, column=1, padx=5, pady=5)

    label4_SvCenterAdr = ttk.Label(SvCenterAdr_window, text='Адрес')
    label4_SvCenterAdr.grid(row=4, column=0, padx=5, pady=5)
    CreateToolTip(label4_SvCenterAdr, text='Адрес')
    entry4_SvCenterAdr = ttk.Entry(SvCenterAdr_window, width=50)
    entry4_SvCenterAdr.grid(row=4, column=1, padx=5, pady=5)

    label10_SvCenterAdr = ttk.Label(SvCenterAdr_window, text='* - необязательные данные')
    label10_SvCenterAdr.grid(row=5, column=0, padx=5, pady=5)

    btn1_SvCenterAdr = ttk.Button(SvCenterAdr_window, text="Сохранить данные",
                                  command=lambda: save_data_svcenteradr(entry0_SvCenterAdr.get(),
                                                                        entry1_SvCenterAdr.get(),
                                                                        entry2_SvCenterAdr.get(),
                                                                        entry3_SvCenterAdr.get(),
                                                                        entry4_SvCenterAdr.get()))
    btn1_SvCenterAdr.grid(row=6, column=1, padx=5, pady=5)


def save_data_svcentercont(string, j, fio, podrazd, dolzhn, rab_tel, mob_tel, el_poch):
    # Проверка введенных данных
    pattern_ORGN = r'^[0-9]{13}$'
    pattern_INN = r'^([0-9][1-9]|[1-9][0-9])[0-9]{8}$'
    pattern_KPP = r'^([0-9][1-9]|[1-9][0-9])([0-9]{2})([0-9A-F]{2})([0-9]{3})$'
    pattern_uri = r'^[a-zA-Z][a-zA-Z0-9+.-]*:([^/\s]+(/[^/\s]*)*)?$'
    patterns_okved = [
        r'^[0-9]{2}$',  # Два числа
        r'^[0-9]{2}\.[0-9]$',  # Два числа, точка, одно число
        r'^[0-9]{2}\.[0-9]{2}$',  # Два числа, точка, два числа
        r'^[0-9]{2}\.[0-9]{2}\.[0-9]$',  # Два числа, точка, два числа, точка, одно число
        r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$',  # Два числа, точка, два числа, точка, два числа
    ]
    global elements

    if string == "СвЦентрКонт":
        FIO.text = fio
        if len(podrazd) > 0:
            Podrazd.text = podrazd
        else:
            SvCentrCont.remove(Podrazd)
        if len(dolzhn) > 0:
            Dolzhn.text = dolzhn
        else:
            SvCentrCont.remove(Dolzhn)
        RabTel.text = rab_tel
        if len(mob_tel) > 0:
            MobTel.text = mob_tel
        else:
            SvCentrCont.remove(MobTel)
        if len(el_poch) > 0:
            ElPoch.text = el_poch
        else:
            SvCentrCont.remove(ElPoch)

        # print(etree.tostring(SvCentrAdr, encoding='unicode', method='xml'))
        # Если валидация прошла успешно, сохраняем данные
        # save_data_to_xml(ogrn_value, inn_value)
        messagebox.showinfo("Успешно", "Данные успешно сохранены")
    else:
        var_name_fio = "FIOUL" + str(j)
        elements[var_name_fio].text = fio
        var_name_podrazd = "PodrazdUL" + str(j)
        if len(podrazd) > 0:
            elements[var_name_podrazd].text = podrazd
        else:
            elements["SvZOContUL"+str(j)].remove(elements[var_name_podrazd])
        var_name_dolzhn = "DolzhnUL" + str(j)
        if len(dolzhn) > 0:
            elements[var_name_dolzhn].text = dolzhn
        else:
            elements["SvZOContUL"+str(j)].remove(elements[var_name_dolzhn])
        var_name_rabtel = "RabTelUL" + str(j)
        elements[var_name_rabtel].text = rab_tel
        var_name_mobtel = "MobTelUL" + str(j)
        if len(mob_tel) > 0:
            elements[var_name_mobtel].text = mob_tel
        else:
            elements["SvZOContUL"+str(j)].remove(elements[var_name_mobtel])
        var_name_elpoch = "ElPochUL" + str(j)
        if len(el_poch) > 0:
            elements[var_name_elpoch].text = el_poch
        else:
            elements["SvZOContUL"+str(j)].remove(elements[var_name_elpoch])

        messagebox.showinfo("Успешно", "Данные успешно сохранены")

    global SvCenterCont_window
    SvCenterCont_window.destroy()


def save_data_svcentercont_dop(fio, podrazd, dolzhn, rab_tel, mob_tel, el_poch):
    global SvCenterCont_Pod_i
    global SvCenterCont1
    global FIO1
    global Podrazd1
    global Dolzhn1
    global RabTel1
    global MobTel1
    global ElPoch1
    # FIO_Pod['ФИО' + str(SvCenterCont_Pod_i)] = etree.SubElement(SvCentrCont, "ФИО")
    FIO1.text = fio
    if len(podrazd) > 0:
        Podrazd1.text = podrazd
    else:
        SvCenterCont1.remove(Podrazd1)
    if len(dolzhn) > 0:
        Dolzhn1.text = dolzhn
    else:
        SvCenterCont1.remove(Dolzhn1)
    RabTel1.text = rab_tel
    if len(mob_tel) > 0:
        MobTel1.text = mob_tel
    else:
        SvCenterCont1.remove(MobTel1)
    if len(el_poch) > 0:
        ElPoch1.text = el_poch
    else:
        SvCenterCont1.remove(ElPoch1)

    # print(etree.tostring(SvCentrAdr, encoding='unicode', method='xml'))
    # Если валидация прошла успешно, сохраняем данные
    # save_data_to_xml(ogrn_value, inn_value)
    global SvCenterCont_window
    SvCenterCont_window.destroy()
    messagebox.showinfo("Успешно", "Данные успешно сохранены")

def SvCenterCont_button_clicked(string, cont_i, j):
    global SvCenterCont_Pod_i
    global SvCenterCont_window
    SvCenterCont_window = Tk()
    SvCenterCont_window.title(string)
    SvCenterCont_window.geometry("900x600")

    label0_SvCenterCont = ttk.Label(SvCenterCont_window, text='ФИО')
    label0_SvCenterCont.grid(row=0, column=0, padx=5, pady=5)
    CreateToolTip(label0_SvCenterCont, text='ФИО контактного лица')
    entry0_SvCenterCont = ttk.Entry(SvCenterCont_window, width=50)
    entry0_SvCenterCont.grid(row=0, column=1, padx=5, pady=5)

    label1_SvCenterCont = ttk.Label(SvCenterCont_window, text='Подразд*')
    label1_SvCenterCont.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(label1_SvCenterCont, text='Подразделение контактного лица')
    entry1_SvCenterCont = ttk.Entry(SvCenterCont_window, width=50)
    entry1_SvCenterCont.grid(row=1, column=1, padx=5, pady=5)

    label2_SvCenterCont = ttk.Label(SvCenterCont_window, text='Должн*')
    label2_SvCenterCont.grid(row=2, column=0, padx=5, pady=5)
    CreateToolTip(label2_SvCenterCont, text='Должность контактного лица')
    entry2_SvCenterCont = ttk.Entry(SvCenterCont_window, width=50)
    entry2_SvCenterCont.grid(row=2, column=1, padx=5, pady=5)

    label3_SvCenterCont = ttk.Label(SvCenterCont_window, text='РабТел')
    label3_SvCenterCont.grid(row=3, column=0, padx=5, pady=5)
    CreateToolTip(label3_SvCenterCont, text='Рабочий телефон контактного лица')
    entry3_SvCenterCont = ttk.Entry(SvCenterCont_window, width=50)
    entry3_SvCenterCont.grid(row=3, column=1, padx=5, pady=5)

    label4_SvCenterCont = ttk.Label(SvCenterCont_window, text='МобТел*')
    label4_SvCenterCont.grid(row=4, column=0, padx=5, pady=5)
    CreateToolTip(label4_SvCenterCont, text='Мобильный телефон контактного лица')
    entry4_SvCenterCont = ttk.Entry(SvCenterCont_window, width=50)
    entry4_SvCenterCont.grid(row=4, column=1, padx=5, pady=5)

    label5_SvCenterCont = ttk.Label(SvCenterCont_window, text='ЭлПоч*')
    label5_SvCenterCont.grid(row=5, column=0, padx=5, pady=5)
    CreateToolTip(label5_SvCenterCont, text='Адрес электронной почты контактного лица')
    entry5_SvCenterCont = ttk.Entry(SvCenterCont_window, width=50)
    entry5_SvCenterCont.grid(row=5, column=1, padx=5, pady=5)

    label10_SvCenterCont = ttk.Label(SvCenterCont_window, text='* - необязательные данные')
    label10_SvCenterCont.grid(row=6, column=0, padx=5, pady=5)

    if cont_i < 1:
        btn1_SvCenterCont = ttk.Button(SvCenterCont_window, text="Сохранить данные",
                                       command=lambda jjj=j, stringg=string: save_data_svcentercont(stringg, jjj, entry0_SvCenterCont.get(),
                                                                              entry1_SvCenterCont.get(),
                                                                              entry2_SvCenterCont.get(),
                                                                              entry3_SvCenterCont.get(),
                                                                              entry4_SvCenterCont.get(),
                                                                              entry5_SvCenterCont.get()))
    else:
        btn1_SvCenterCont = ttk.Button(SvCenterCont_window, text="Сохранить данные",
                                       command=lambda: save_data_svcentercont_dop(entry0_SvCenterCont.get(),
                                                                                  entry1_SvCenterCont.get(),
                                                                                  entry2_SvCenterCont.get(),
                                                                                  entry3_SvCenterCont.get(),
                                                                                  entry4_SvCenterCont.get(),
                                                                                  entry5_SvCenterCont.get()))
    btn1_SvCenterCont.grid(row=7, column=1, padx=5, pady=5)


global SvCenterCont_Pod_i
SvCenterCont_Pod_i = 0


def PlusSvCenterCont_button_clicked(string):
    global SvCenterCont_Pod_i
    SvCenterCont_Pod_i = 1
    global SvCenterCont1
    global FIO1
    global Podrazd1
    global Dolzhn1
    global RabTel1
    global MobTel1
    global ElPoch1
    if SvCenterCont_Pod_i == 1:
        first_svn_cont = SvCentrGS.find(".//СвЦентрКонт")
        SvCenterCont1 = etree.Element("СвЦентрКонт")
        first_svn_cont.addnext(SvCenterCont1)
        # SvCenterCont1 = etree.SubElement(SvCentrGS, "СвЦентрКонт")
        FIO1 = etree.SubElement(SvCenterCont1, "ФИО")
        Podrazd1 = etree.SubElement(SvCenterCont1, "Подразд")
        Dolzhn1 = etree.SubElement(SvCenterCont1, "Должн")
        RabTel1 = etree.SubElement(SvCenterCont1, "РабТел")
        MobTel1 = etree.SubElement(SvCenterCont1, "МобТел")
        ElPoch1 = etree.SubElement(SvCenterCont1, "ЭлПоч")

        global index_row
        # index_row = index_row + 1

        # btn_key = str(SvCenterCont_Pod_i)
        global btn7
        btn7 = ttk.Button(text='СвЦентрКонт', command=lambda: SvCenterCont_button_clicked("СвЦентрКонт", 1, 0))

        # Размещение кнопки на макете
        btn7.grid(row=index_row, column=1, padx=5, pady=5)
        CreateToolTip(btn7, text='Сведения о дополнительном контактном лице центра ГосСОПКА по вопросам взаимодействия')


def MinusSvCenterCont_button_clicked(string):
    global SvCenterCont_Pod_i
    # SvCenterCont_Pod_i = SvCenterCont_Pod_i - 1
    SvCenterCont_Pod_i = 0
    if SvCenterCont_Pod_i == 0:
        btn7.destroy()
        SvCentrGS.remove(SvCenterCont1)
        # SvCentrCont.remove(FIO1)
        # SvCentrCont.remove(Podrazd1)
        # SvCentrCont.remove(Dolzhn1)
        # SvCentrCont.remove(RabTel1)
        # SvCentrCont.remove(MobTel1)
        # SvCentrCont.remove(ElPoch1)


def SvZonaOtv_button_clicked(string):
    global SvZonaOtv_window
    SvZonaOtv_window = Tk()
    SvZonaOtv_window.title(string)
    SvZonaOtv_window.geometry("900x600")

    global edzo_i
    edzo_i = 0
    global btn30_elems
    btn30_elems = {}
    global elements
    elements = {}

    label11_SvZonaOtv = ttk.Label(SvZonaOtv_window, text="")
    label11_SvZonaOtv.grid(row=0, column=0, padx=70, pady=5)

    btn11_SvZonaOtv = ttk.Button(SvZonaOtv_window, text="Добавить единицу зоны ответственности центра",
                                 command=add_edzo)
    btn11_SvZonaOtv.grid(row=0, column=1, padx=5, pady=5)

    btn12_SvZonaOtv = ttk.Button(SvZonaOtv_window, text="Удалить единицу зоны ответственности центра",
                                 command=del_edzo)
    btn12_SvZonaOtv.grid(row=0, column=2, padx=5, pady=5)


def del_edzo():
    global SvZonaOtv_window
    global edzo_i
    global btn30_name
    global btn30_elems
    btn30_name = "btn30_" + str(edzo_i)
    btn30_elems[btn30_name].destroy()
    del btn30_elems[btn30_name]
    if edzo_i > 0:
        edzo_i = edzo_i - 1
    return


def add_edzo():
    global SvZonaOtv_window
    global edzo_i
    edzo_i = edzo_i + 1

    global btn30_elems
    global btn30_name

    btn30_name = "btn30_" + str(edzo_i)

    btn30_elems[btn30_name] = ttk.Button(SvZonaOtv_window, text="ЕдЗО " + str(edzo_i),
                                         command=lambda j=edzo_i: EdZO_button_clicked(j))
    btn30_elems[btn30_name].grid(row=edzo_i, column=0, padx=5, pady=5)
    CreateToolTip(btn30_elems[btn30_name], text='Единица зоны ответственности центра ГосСОПКА')


def EdZO_button_clicked(j):
    # global edzo_i

    global elements

    # Создание главного элемента
    var_name = "EdZO" + str(j)
    if var_name not in elements:
        elements[var_name] = etree.SubElement(SvZonaOtv, "ЕдЗО")

        # Создание подэлементов и установка атрибутов для SvZOUL
        var_name = "SvZOUL" + str(j)
        elements[var_name] = etree.SubElement(elements["EdZO" + str(j)], "СвЗОЮЛ")

        elements[var_name].set("ОРГН", "value")
        elements[var_name].set("ИНН", "value")
        elements[var_name].set("КПП", "value")
        elements[var_name].set("НаимЮЛПолн", "value")
        elements[var_name].set("НаимЮЛСокр", "value")
        elements[var_name].set("Тип", "value")
        elements[var_name].set("Сайт", "value")
        elements[var_name].set("ОКВЭД", "value")
        elements[var_name].set("ОКОГУ", "value")
        elements[var_name].set("ОКОПФ", "value")

        # Создание подэлементов для SvZOContUL и установка атрибутов
        var_name = "SvZOContUL" + str(j)
        elements[var_name] = etree.SubElement(elements["EdZO" + str(j)], "СвЗОКонтЮЛ")

        var_name_fio = "FIOUL" + str(j)
        elements[var_name_fio] = etree.SubElement(elements["SvZOContUL" + str(j)], "ФИО")

        var_name_podrazd = "PodrazdUL" + str(j)
        elements[var_name_podrazd] = etree.SubElement(elements["SvZOContUL" + str(j)], "Подразд")  # Необязательно

        var_name_dolzhn = "DolzhnUL" + str(j)
        elements[var_name_dolzhn] = etree.SubElement(elements["SvZOContUL" + str(j)], "Должн")  # Необязательно

        var_name_rabtel = "RabTelUL" + str(j)
        elements[var_name_rabtel] = etree.SubElement(elements["SvZOContUL" + str(j)], "РабТел")

        var_name_mobtel = "MobTelUL" + str(j)
        elements[var_name_mobtel] = etree.SubElement(elements["SvZOContUL" + str(j)], "МобТел")  # Необязательно

        var_name_elpoch = "ElPochUL" + str(j)
        elements[var_name_elpoch] = etree.SubElement(elements["SvZOContUL" + str(j)], "ЭлПоч")  # Необязательно

        # Создание подэлементов для SvZOObktUL и SvZOULSeti
        var_name_obkt = "SvZOObktUL" + str(j)
        elements[var_name_obkt] = etree.SubElement(elements["EdZO" + str(j)], "СвЗООбктЮЛ")

        var_name_seti = "SvZOULSeti" + str(j)
        elements[var_name_seti] = etree.SubElement(elements["EdZO" + str(j)], "СвЗОЮЛСети")

    EdZO_window = Tk()
    EdZO_window.title("ЕдЗО" + str(j))
    EdZO_window.geometry("900x600")

    btn1 = ttk.Button(EdZO_window, text="СвЗОЮЛ", command=lambda j1=j: SvUL_button_clicked("СвЗОЮЛ", j1))
    btn1.grid(row=0, column=0, padx=5, pady=5)
    CreateToolTip(btn1, text='Сведения о юридическом лице, чьи информационные ресурсы принимаются в зону '
                             'ответственности центра ГосСОПКА')

    btn1 = ttk.Button(EdZO_window, text="СвЗОКонтЮЛ", command=lambda j2=j: SvCenterCont_button_clicked("СвЗОКонтЮЛ", 0, j2))
    btn1.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(btn1, text='Сведения о контактном лице юридического лица, чьи информационные ресурсы передаются в '
                             'зону ответственности центра ГосСОПКА')

    btn1 = ttk.Button(EdZO_window, text="СвЗООбктЮЛ", command=lambda j3=j: SvZOObktUL_button_clicked("СвЗООбктЮЛ", j3))
    btn1.grid(row=2, column=0, padx=5, pady=5)
    CreateToolTip(btn1, text='Сведения об информационных ресурсах, принадлежащих юридическому лицу, которые '
                             'передаются в зону ответственности центра ГосСОПКА')

    btn1 = ttk.Button(EdZO_window, text="СвЗОЮЛСети", command=lambda j4=j: SvZOULSeti_button_clicked("СвЗОЮЛСети", j4))
    btn1.grid(row=3, column=0, padx=5, pady=5)
    CreateToolTip(btn1, text='Сведения о сетевых информационных ресурсах, принадлежащих юридическому лицу, которые '
                             'передаются в зону ответственности центра ГосСОПКА')


def save_data_svul_2(string, j, ogrn_value, inn_value, kpp_value, naim_poln, naim_sokr, tip, site, okved, okogu, okopf):
    if string == "СвЮЛ":
        SvULTip.set("ОРГН", ogrn_value)  # required
        SvULTip.set("ИНН", inn_value)  # required
        SvULTip.set("КПП", kpp_value)  # required
        SvULTip.set("НаимЮЛПолн", naim_poln)  # required
        if len(naim_sokr) > 0:
            SvULTip.set("НаимЮЛСокр", naim_sokr)
        else:
            del SvULTip.attrib["НаимЮЛСокр"]
        SvULTip.set("Тип", tip)  # required
        if len(site) > 0:
            SvULTip.set("Сайт", site)
        else:
            del SvULTip.attrib["Сайт"]
        SvULTip.set("ОКВЭД", okved)  # required
        if len(okogu) > 0:
            SvULTip.set("ОКОГУ", okogu)
        else:
            del SvULTip.attrib["ОКОГУ"]
        if len(okopf) > 0:
            SvULTip.set("ОКОПФ", okopf)
        else:
            del SvULTip.attrib["ОКОПФ"]

        # print(etree.tostring(SvULTip).decode())
        # Если валидация прошла успешно, сохраняем данные
        # save_data_to_xml(ogrn_value, inn_value)
        messagebox.showinfo("Успешно", "Данные успешно сохранены")
    else:
        var_name = "SvZOUL" + str(j)

        elements[var_name].set("ОРГН", ogrn_value)  # required
        elements[var_name].set("ИНН", inn_value)  # required
        elements[var_name].set("КПП", kpp_value)  # required
        elements[var_name].set("НаимЮЛПолн", naim_poln)  # required
        if len(naim_sokr) > 0:
            elements[var_name].set("НаимЮЛСокр", naim_sokr)
        else:
            del elements[var_name].attrib["НаимЮЛСокр"]
        elements[var_name].set("Тип", tip)  # required
        if len(site) > 0:
            elements[var_name].set("Сайт", site)
        else:
            del elements[var_name].attrib["Сайт"]
        elements[var_name].set("ОКВЭД", okved)  # required
        if len(okogu) > 0:
            elements[var_name].set("ОКОГУ", okogu)
        else:
            del elements[var_name].attrib["ОКОГУ"]
        if len(okopf) > 0:
            elements[var_name].set("ОКОПФ", okopf)
        else:
            del elements[var_name].attrib["ОКОПФ"]
        messagebox.showinfo("Успешно", "Данные успешно сохранены")


def SvZOObktUL_button_clicked(string, jj):
    global SvZOObktUL_window
    SvZOObktUL_window = Tk()
    SvZOObktUL_window.title(string)
    SvZOObktUL_window.geometry("900x600")

    global SvZOObktUL_i
    SvZOObktUL_i = 0
    global btn40_elems
    btn40_elems = {}
    global elementss
    elementss = {}
    global elementsss
    elementsss = {}

    label11_SvZOObktUL = ttk.Label(SvZOObktUL_window, text="")
    label11_SvZOObktUL.grid(row=0, column=0, padx=70, pady=5)

    btn11_SvZOObktUL = ttk.Button(SvZOObktUL_window, text="Добавить СвОбкт", command=lambda jj1=jj: add_svobkt(jj1))
    btn11_SvZOObktUL.grid(row=0, column=1, padx=5, pady=5)
    CreateToolTip(btn11_SvZOObktUL,
                  text='Добавить cведения об информационном ресурсе, который передается в зону ответственности центра ГосСОПКА')

    btn12_SvZOObktUL = ttk.Button(SvZOObktUL_window, text="Удалить СвОбкт",
                                  command=lambda jj2=jj: del_svobkt(jj2))
    btn12_SvZOObktUL.grid(row=0, column=2, padx=5, pady=5)
    CreateToolTip(btn12_SvZOObktUL,
                  text='Удалить cведения об информационном ресурсе, которыйпередается в зону ответственности центра ГосСОПКА')


def del_svobkt(jj):
    global SvZOObktUL_window
    global SvZOObktUL_i
    global btn40_name
    global btn40_elems
    btn40_name = "btn40_" + str(jj) + str(SvZOObktUL_i)
    btn40_elems[btn40_name].destroy()
    del btn40_elems[btn40_name]
    if SvZOObktUL_i > 0:
        SvZOObktUL_i = SvZOObktUL_i - 1
    return


def add_svobkt(jj):
    global SvZOObktUL_window
    global SvZOObktUL_i
    SvZOObktUL_i = SvZOObktUL_i + 1

    global btn40_elems
    global btn40_name

    btn40_name = "btn40_" + str(jj) + str(SvZOObktUL_i)

    btn40_elems[btn40_name] = ttk.Button(SvZOObktUL_window,
                                         text="ЕдЗО " + str(jj) + ". " + "СвОбкт " + str(SvZOObktUL_i),
                                         command=lambda j=SvZOObktUL_i, jj2=jj: SvObkt_button_clicked(j, jj2))
    btn40_elems[btn40_name].grid(row=SvZOObktUL_i, column=0, padx=5, pady=5)
    CreateToolTip(btn40_elems[btn40_name],
                  text='Сведения об информационном ресурсе, который передается в зону ответственности центра ГосСОПКА')


def SvObkt_button_clicked(j, jj):
    # global edzo_i

    global elements
    global elementss

    global Funk_i
    global cmbox60_elems
    Funk_i = 0
    cmbox60_elems = {}

    # Создание главного элемента
    obkt_name = "SvZOObktUL" + str(jj)
    var_name = "SvObkt" + str(jj) + "." + str(j)
    global AdrRazm_i
    AdrRazm_i = 1
    if var_name not in elementss:
        elementss[var_name] = etree.SubElement(elements[obkt_name], "СвОбкт")
        elementss[var_name].set("Наим", "value")
        # Создание подэлементов и установка атрибутов для SvObkt

        var_name = "SvKII" + str(jj) + "." + str(j)
        elementss[var_name] = etree.SubElement(elementss["SvObkt" + str(jj) + "." + str(j)], "СвКИИ")
        '''
        var_name = "RegNom" + str(jj) + "." + str(j)
        elementss[var_name] = etree.SubElement(elementss["SvKII" + str(jj) + "." + str(j)], "РегНом")

        var_name = "KatZnach" + str(jj) + "." + str(j)
        elementss[var_name] = etree.SubElement(elementss["SvKII" + str(jj) + "." + str(j)], "КатЗнач")
        '''
        var_name = "SvFunktcii" + str(jj) + "." + str(j)
        elementss[var_name] = etree.SubElement(elementss["SvObkt" + str(jj) + "." + str(j)], "СвФункции")

        var_name = "SvAdrRazm" + str(jj) + "." + str(j)
        elementss[var_name] = etree.SubElement(elementss["SvObkt" + str(jj) + "." + str(j)], "СвАдрРазм")


    global SvObkt_window
    SvObkt_window = Tk()
    SvObkt_window.title("СвОбкт" + str(jj) + "." + str(j))
    SvObkt_window.geometry("900x600")
    global SvDoc_i
    global btn50_elems
    global btn50_name
    SvDoc_i = 0
    btn50_elems = {}
    btn50_name = "btn50_" + str(jj) + "." + str(j) + str(SvDoc_i)

    btn1 = ttk.Button(SvObkt_window, text="Добавить СвДокумент",
                      command=lambda j1=j, jj1=jj: add_svdoc("СвДокумент", j1, jj1))
    btn1.grid(row=0, column=0, padx=5, pady=5)

    btn1 = ttk.Button(SvObkt_window, text="Удалить СвДокумент",
                      command=lambda j2=j, jj2=jj: del_svdoc("СвДокумент", j2, jj2))
    btn1.grid(row=0, column=1, padx=5, pady=5)

    btn50_elems[btn50_name] = ttk.Button(SvObkt_window, text="СвДокумент",
                                         command=lambda Doc_i=SvDoc_i, j3=j, jj3=jj: SvDocument_button_clicked("СвДокумент", j3, jj3,
                                                                                                 Doc_i))
    btn50_elems[btn50_name].grid(row=1, column=SvDoc_i, padx=5, pady=5)
    CreateToolTip(btn50_elems[btn50_name],
                  text='Сведения о документе, на основании которого информационный ресурс передается в зону ответственности центра ГосСОПКА')

    label11_SvZOObktUL = ttk.Label(SvObkt_window, text="")
    label11_SvZOObktUL.grid(row=2, column=0, padx=70, pady=10)

    btn1 = ttk.Button(SvObkt_window, text="СвКИИ", command=lambda j4=j, jj4=jj: SvKII_button_clicked("СвКИИ", j4, jj4))
    btn1.grid(row=3, column=0, padx=5, pady=5)
    CreateToolTip(btn1,
                  text='Сведения о принадлежности информационного ресурса, который передается в зону ответственности центра ГосСОПКА, критической информационной инфраструктуре Российской Федерации')

    btn1 = ttk.Button(SvObkt_window, text="СвФункции", command=lambda j5=j, jj5=jj: SvFunktcii_button_clicked("СвФункции", j5, jj5))
    btn1.grid(row=4, column=0, padx=5, pady=5)
    CreateToolTip(btn1,
                  text='Сведения о функциях, реализуемых центром ГосСОПКА в отношении информационного ресурса, который передается в зону ответственности центра ГосСОПКА')

    btn1 = ttk.Button(SvObkt_window, text="СвАдрРазм", command=lambda j6=j, jj6=jj: SvAdrRazm_button_clicked("СвАдрРазм", j6, jj6))
    btn1.grid(row=5, column=0, padx=5, pady=5)
    CreateToolTip(btn1,
                  text='Сведения об адресах размещения информационного ресурса, который передается в зону ответственности центра ГосСОПКА')


def add_svdoc(string, j, jj):
    global SvObkt_window
    global SvDoc_i
    global btn50_elems
    global btn50_name
    if SvDoc_i < 14:
        SvDoc_i = SvDoc_i + 1
        btn50_name = "btn50_" + str(jj) + "." + str(j) + str(SvDoc_i)

        btn50_elems[btn50_name] = ttk.Button(SvObkt_window, text="СвДокумент",
                                             command=lambda Doc_i=SvDoc_i, j7=j, jj7=jj: SvDocument_button_clicked("СвДокумент", j7,
                                                                                                     jj7,
                                                                                                     Doc_i))
        btn50_elems[btn50_name].grid(row=1, column=SvDoc_i, padx=5, pady=5)
        CreateToolTip(btn50_elems[btn50_name],
                      text='Сведения о документе, на основании которого информационный ресурс передается в зону ответственности центра ГосСОПКА')


def del_svdoc(string, j, jj):
    global SvObkt_window
    global SvDoc_i
    global btn50_elems
    global btn50_name

    btn50_name = "btn50_" + str(jj) + "." + str(j) + str(SvDoc_i)
    btn50_elems[btn50_name].destroy()
    del btn50_elems[btn50_name]
    if SvDoc_i > 1:
        SvDoc_i = SvDoc_i - 1


def SvDocument_button_clicked(string, j, jj, Doc_i):
    global SvDocument_window
    SvDocument_window = Tk()
    SvDocument_window.title("СвДокумент")
    SvDocument_window.geometry("900x600")

    global elementsss
    global elementss

    # Создание главного элемента
    var_name = "SvDocument" + str(jj) + "." + str(j) + str(Doc_i)
    if var_name not in elementsss:
        # Создание подэлементов и установка атрибутов для SvObkt
        elementsss[var_name] = etree.SubElement(elementss["SvObkt" + str(jj) + "." + str(j)], "СвДокумент")

        var_name = "Naim" + str(jj) + "." + str(j) + str(Doc_i)
        elementsss[var_name] = etree.SubElement(elementsss["SvDocument" + str(jj) + "." + str(j) + str(Doc_i)], "Наим")

        var_name = "DataStart" + str(jj) + "." + str(j) + str(Doc_i)
        elementsss[var_name] = etree.SubElement(elementsss["SvDocument" + str(jj) + "." + str(j) + str(Doc_i)], "ДатаСтарт")

        var_name = "DataFinish" + str(jj) + "." + str(j) + str(Doc_i)
        elementsss[var_name] = etree.SubElement(elementsss["SvDocument" + str(jj) + "." + str(j) + str(Doc_i)], "ДатаФиниш")

        var_name = "Rekv" + str(jj) + "." + str(j) + str(Doc_i)
        elementsss[var_name] = etree.SubElement(elementsss["SvDocument" + str(jj) + "." + str(j) + str(Doc_i)], "Рекв")

        var_name = "Com" + str(jj) + "." + str(j) + str(Doc_i)
        elementsss[var_name] = etree.SubElement(elementsss["SvDocument" + str(jj) + "." + str(j) + str(Doc_i)], "Ком")

    label5_SvDocument = ttk.Label(SvDocument_window, text='Наим')
    label5_SvDocument.grid(row=0, column=0, padx=5, pady=5)
    CreateToolTip(label5_SvDocument, text='Наименование документа, на основании которого информационный ресурс передается в зону ответственности')
    entry1_SvDocument = ttk.Entry(SvDocument_window, width=50)
    entry1_SvDocument.grid(row=0, column=1, padx=5, pady=5)

    label5_SvDocument = ttk.Label(SvDocument_window, text='ДатаСтарт: YYYY-MM-DD')
    label5_SvDocument.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(label5_SvDocument, text='Дата начала действия документа, на основании которого информационный ресурс передается в зону ответственности')
    entry2_SvDocument = ttk.Entry(SvDocument_window, width=50)
    entry2_SvDocument.grid(row=1, column=1, padx=5, pady=5)

    label5_SvDocument = ttk.Label(SvDocument_window, text='ДатаФиниш: YYYY-MM-DD')
    label5_SvDocument.grid(row=2, column=0, padx=5, pady=5)
    CreateToolTip(label5_SvDocument, text='Дата окончания действия документа, на основании которого информационный ресурс передается в зону ответственности')
    entry3_SvDocument = ttk.Entry(SvDocument_window, width=50)
    entry3_SvDocument.grid(row=2, column=1, padx=5, pady=5)

    label5_SvDocument = ttk.Label(SvDocument_window, text='Рекв')
    label5_SvDocument.grid(row=3, column=0, padx=5, pady=5)
    CreateToolTip(label5_SvDocument, text='Реквизиты документа, на основании которого информационный ресурс передается в зону ответственности')
    entry4_SvDocument = ttk.Entry(SvDocument_window, width=50)
    entry4_SvDocument.grid(row=3, column=1, padx=5, pady=5)

    label5_SvDocument = ttk.Label(SvDocument_window, text='Ком*')
    label5_SvDocument.grid(row=4, column=0, padx=5, pady=5)
    CreateToolTip(label5_SvDocument, text='Комментарий к документу, на основании которого информационный ресурс передается в зону ответственности')
    entry5_SvDocument = ttk.Entry(SvDocument_window, width=50)
    entry5_SvDocument.grid(row=4, column=1, padx=5, pady=5)

    label10_SvDocument = ttk.Label(SvDocument_window, text='* - необязательные данные')
    label10_SvDocument.grid(row=5, column=0, padx=5, pady=5)

    btn1_SvDocument = ttk.Button(SvDocument_window, text="Сохранить данные",
                                       command=lambda j1=j, jj1=jj, Doc_i1=Doc_i: save_data_document(j1, jj1, Doc_i1, entry1_SvDocument.get(),entry2_SvDocument.get(),entry3_SvDocument.get(),entry4_SvDocument.get(),entry5_SvDocument.get()))
    btn1_SvDocument.grid(row=6, column=1, padx=5, pady=5)


def save_data_document(j, jj, Doc_i, naim, datastart, datafinish, rekk, com):
    global elementsss

    var_name_naim = "Naim" + str(jj) + "." + str(j) + str(Doc_i)
    elementsss[var_name_naim].text = naim

    var_name_naim = "DataStart" + str(jj) + "." + str(j) + str(Doc_i)
    elementsss[var_name_naim].text = datastart

    var_name_naim = "DataFinish" + str(jj) + "." + str(j) + str(Doc_i)
    elementsss[var_name_naim].text = datafinish

    var_name_naim = "Rekv" + str(jj) + "." + str(j) + str(Doc_i)
    elementsss[var_name_naim].text = rekk

    var_name_podrazd = "Com" + str(jj) + "." + str(j) + str(Doc_i)
    if len(com) > 0:
        elementsss[var_name_podrazd].text = com
    else:
        elementsss["SvDocument" + str(jj) + "." + str(j) + str(Doc_i)].remove(elementsss[var_name_podrazd])

    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global SvDocument_window
    SvDocument_window.destroy()


def SvKII_button_clicked(string, j, jj):
    global SvKII_window
    SvKII_window = Tk()
    SvKII_window.title("СвКИИ")
    SvKII_window.geometry("900x600")

    label1_SvKII = ttk.Label(SvKII_window, text='РегНом*')
    label1_SvKII.grid(row=0, column=0, padx=5, pady=5)
    CreateToolTip(label1_SvKII,
                  text='Регистрационный номер значимого объекта критической информационной инфраструктуры Российской Федераци')
    entry1_SvKII = ttk.Entry(SvKII_window, width=50)
    entry1_SvKII.grid(row=0, column=1, padx=5, pady=5)

    label2_SvKII = ttk.Label(SvKII_window, text='КатЗнач*')
    label2_SvKII.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(label2_SvKII,
                  text='Категория значимости объекта критической информационной инфраструктуры Российской Федерации')
    entry2_SvKII = ttk.Entry(SvKII_window, width=50)
    entry2_SvKII.grid(row=1, column=1, padx=5, pady=5)

    label3_SvKII = ttk.Label(SvKII_window, text='* - необязательные данные')
    label3_SvKII.grid(row=3, column=0, padx=5, pady=5)

    btn1_SvKII = ttk.Button(SvKII_window, text="Сохранить данные",
                                 command=lambda j1=j, jj1=jj: save_kii(j1, jj1, entry1_SvKII.get(), entry2_SvKII.get()))
    btn1_SvKII.grid(row=4, column=1, padx=5, pady=5)


def save_kii(j,jj,regnom,katznach):
    global elementss

    var_name = "RegNom" + str(jj) + "." + str(j)
    elementss[var_name] = etree.SubElement(elementss["SvKII" + str(jj) + "." + str(j)], "РегНом")

    var_name = "KatZnach" + str(jj) + "." + str(j)
    elementss[var_name] = etree.SubElement(elementss["SvKII" + str(jj) + "." + str(j)], "КатЗнач")

    var_name = "RegNom" + str(jj) + "." + str(j)
    elementss[var_name].text = regnom

    var_name = "KatZnach" + str(jj) + "." + str(j)
    elementss[var_name].text = katznach
    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global SvKII_window
    SvKII_window.destroy()


def SvFunktcii_button_clicked(string, j, jj):
    global SvFunk_window
    SvFunk_window = Tk()
    SvFunk_window.title("СвФункции")
    SvFunk_window.geometry("900x600")

    global Funk_i
    global cmbox60_elems
    global cmbox60_name

    cmbox60_name = "cmbox60_" + str(jj) + str(j) + str(Funk_i)

    btn1 = ttk.Button(SvFunk_window, text="Добавить СвФункцию",
                      command=lambda j1=j, jj1=jj: add_svfunk("СвФункция", j1, jj1))
    btn1.grid(row=0, column=1, padx=5, pady=5)

    btn1 = ttk.Button(SvFunk_window, text="Удалить СвФункцию",
                      command=lambda j2=j, jj2=jj: del_svfunk("СвФункция", j2, jj2))
    btn1.grid(row=0, column=2, padx=5, pady=5)

    Funki = ['ВЗАИМОДЕЙСТВИЕ С НКЦКИ', 'РАЗРАБОТКА ДОКУМЕНТОВ ОПКА', 'ЭКСПЛУАТАЦИЯ СРЕДСТВ ГОССОПКА', 'ПРИЕМ СООБЩЕНИЙ ОБ ИНЦИДЕНТАХ', 'РЕГИСТРАЦИЯ КА И КИ', 'АНАЛИЗ СОБЫТИЙ ИБ', 'ИНВЕНТАРИЗАЦИЯ ИР', 'АНАЛИЗ УГРОЗ ИБ', 'СОСТАВЛЕНИЕ И АКТУАЛИЗАЦИЯ ПЕРЕЧНЯ УГРОЗ ИБ', 'ВЫЯВЛЕНИЕ УЯЗВИМОСТЕЙ ИР', 'ФОРМИРОВАНИЕ ПРЕДЛОЖЕНИЙ ПО ПОВЫШЕНИЮ УРОВНЯ ЗАЩИЩЕННОСТИ ИР', 'СОСТАВЛЕНИЕ ПЕРЕЧНЯ КИ', 'ЛИКВИДАЦИЯ ПОСЛЕДСТВИЙ КИ', 'АНАЛИЗ РЕЗУЛЬТАТОВ ЛИКВИДАЦИИ ПОСЛЕДСТВИЙ КИ', 'УСТАНОВЛЕНИЕ ПРИЧИН КИ']
    label3 = ttk.Label(SvFunk_window, text='Функции')
    label3.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(label3, text='Наименование функции, реализуемой в отношении информационного ресурса')
    cmbox60_elems[cmbox60_name] = ttk.Combobox(SvFunk_window, values=Funki, state='readonly', width=85)
    cmbox60_elems[cmbox60_name].grid(row=Funk_i+1, column=1, padx=20, pady=5)
    cmbox60_elems[cmbox60_name].bind("<<ComboboxSelected>>", lambda Funk_ii=Funk_i, j3=j, jj3=jj: SvFunktiya_button_clicked("СвФункция", j3, jj3, Funk_ii, cmbox60_elems[cmbox60_name].get()))

    btn1_SvFunk = ttk.Button(SvFunk_window, text="Сохранить данные",
                                 command=save_funktcii)
    btn1_SvFunk.grid(row=4, column=2, padx=5, pady=5)


def add_svfunk(string, j, jj):
    global Funk_i
    global SvFunk_window
    global cmbox60_elems
    global cmbox60_name
    if Funk_i < 14:
        Funk_i = Funk_i + 1
        cmbox60_name = "cmbox60_" + str(jj) + str(j) + str(Funk_i)
        #var_name = "Funktciya" + str(jj) + "." + str(j) + str(Funk_i)
        #elementss[var_name] = etree.SubElement(elementss["SvFunktcii" + str(jj) + "." + str(j)], "Функция")
        Funki = ['ВЗАИМОДЕЙСТВИЕ С НКЦКИ', 'РАЗРАБОТКА ДОКУМЕНТОВ ОПКА', 'ЭКСПЛУАТАЦИЯ СРЕДСТВ ГОССОПКА',
                 'ПРИЕМ СООБЩЕНИЙ ОБ ИНЦИДЕНТАХ', 'РЕГИСТРАЦИЯ КА И КИ', 'АНАЛИЗ СОБЫТИЙ ИБ', 'ИНВЕНТАРИЗАЦИЯ ИР',
                 'АНАЛИЗ УГРОЗ ИБ', 'СОСТАВЛЕНИЕ И АКТУАЛИЗАЦИЯ ПЕРЕЧНЯ УГРОЗ ИБ', 'ВЫЯВЛЕНИЕ УЯЗВИМОСТЕЙ ИР',
                 'ФОРМИРОВАНИЕ ПРЕДЛОЖЕНИЙ ПО ПОВЫШЕНИЮ УРОВНЯ ЗАЩИЩЕННОСТИ ИР', 'СОСТАВЛЕНИЕ ПЕРЕЧНЯ КИ',
                 'ЛИКВИДАЦИЯ ПОСЛЕДСТВИЙ КИ', 'АНАЛИЗ РЕЗУЛЬТАТОВ ЛИКВИДАЦИИ ПОСЛЕДСТВИЙ КИ', 'УСТАНОВЛЕНИЕ ПРИЧИН КИ']

        cmbox60_elems[cmbox60_name] = ttk.Combobox(SvFunk_window, values=Funki, state='readonly', width=85)
        cmbox60_elems[cmbox60_name].grid(row=Funk_i+1, column=1, padx=20, pady=5)
        cmbox60_elems[cmbox60_name].bind("<<ComboboxSelected>>",
                                         lambda Funk_ii=Funk_i, j4=j, jj4=jj: SvFunktiya_button_clicked("СвФункция", j4, jj4, Funk_ii, cmbox60_elems[cmbox60_name].get()))

    return


def del_svfunk(string, j, jj):
    global Funk_i
    global SvFunk_window
    global cmbox60_elems
    global cmbox60_name

    cmbox60_name = "cmbox60_" + str(jj) + str(j) + str(Funk_i)
    cmbox60_elems[cmbox60_name].destroy()
    del cmbox60_elems[cmbox60_name]
    if Funk_i > 1:
        Funk_i = Funk_i - 1
    return


def SvFunktiya_button_clicked(string, j, jj, Funk_ii, f):
    global Funk_i

    global elementss

    var_name = "Funktciya" + str(jj) + "." + str(j) + str(Funk_i)
    elementss[var_name] = etree.SubElement(elementss["SvFunktcii" + str(jj) + "." + str(j)], "Функция")

    elementss[var_name].text = f


def save_funktcii():
    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global SvFunk_window
    SvFunk_window.destroy()


def SvAdrRazm_button_clicked(string, j, jj):
    global SvAdrRazm_window
    SvAdrRazm_window = Tk()
    SvAdrRazm_window.title("СвАдрРазм"  + str(jj) + "." + str(j))
    SvAdrRazm_window.geometry("900x600")

    global elementss
    global AdrRazm_i
    global btn80_elems
    btn80_elems = {}
    btn80_name = "btn80_" + str(jj) + "." + str(j) + str(AdrRazm_i)

    btn1 = ttk.Button(SvAdrRazm_window, text="Добавить АдрРазмОбкт",
                      command=lambda j1=j, jj1=jj: add_adr("АдрРазмОбкт", j1, jj1))
    btn1.grid(row=0, column=0, padx=5, pady=5)

    btn1 = ttk.Button(SvAdrRazm_window, text="Удалить АдрРазмОбкт",
                      command=lambda j2=j, jj2=jj: del_adr("АдрРазмОбкт", j2, jj2))
    btn1.grid(row=0, column=1, padx=5, pady=5)

    btn80_elems[btn80_name] = ttk.Button(SvAdrRazm_window, text="АдрРазмОбкт",
                                         command=lambda Doc_ii=AdrRazm_i, j3=j, jj3=jj: AdrRazmObkt_button_clicked(
                                             "АдрРазмОбкт", j3, jj3,
                                             Doc_ii))
    btn80_elems[btn80_name].grid(row=AdrRazm_i, column=1, padx=5, pady=5)
    CreateToolTip(btn80_elems[btn80_name],
                  text='Адрес размещения информационного ресурса')

    return


def add_adr(string, j, jj):
    global SvAdrRazm_window
    global AdrRazm_i
    global elementss
    global btn80_elems

    AdrRazm_i = AdrRazm_i + 1
    btn80_name = "btn80_" + str(jj) + "." + str(j) + str(AdrRazm_i)
    btn80_elems[btn80_name] = ttk.Button(SvAdrRazm_window, text="АдрРазмОбкт",
                                         command=lambda Doc_ii=AdrRazm_i, j3=j, jj3=jj: AdrRazmObkt_button_clicked(
                                             "АдрРазмОбкт", j3, jj3,
                                             Doc_ii))
    btn80_elems[btn80_name].grid(row=AdrRazm_i, column=1, padx=5, pady=5)
    CreateToolTip(btn80_elems[btn80_name],
                  text='Адрес размещения информационного ресурса')

    return


def del_adr(string, j, jj):
    global SvAdrRazm_window
    global AdrRazm_i
    global elementss
    global btn80_elems
    if AdrRazm_i > 1:
        btn80_name = "btn80_" + str(jj) + "." + str(j) + str(AdrRazm_i)
        btn80_elems[btn80_name].destroy()
        del btn80_elems[btn80_name]
        AdrRazm_i = AdrRazm_i - 1

    return


def AdrRazmObkt_button_clicked(string, j, jj, Doc_ii):
    global AdrRazmObkt_window
    AdrRazmObkt_window = Tk()
    AdrRazmObkt_window.title("СвАдрРазм" + str(jj) + "." + str(j))
    AdrRazmObkt_window.geometry("900x600")

    label0_SvCenterAdr = ttk.Label(AdrRazmObkt_window, text='КодРегион')
    label0_SvCenterAdr.grid(row=0, column=0, padx=5, pady=5)
    CreateToolTip(label0_SvCenterAdr, text='Код субъекта Российской Федерации')
    entry0_SvCenterAdr = ttk.Entry(AdrRazmObkt_window, width=50)
    entry0_SvCenterAdr.grid(row=0, column=1, padx=5, pady=5)

    label1_SvCenterAdr = ttk.Label(AdrRazmObkt_window, text='НаимРегион')
    label1_SvCenterAdr.grid(row=1, column=0, padx=5, pady=5)
    CreateToolTip(label1_SvCenterAdr, text='Наименование субъекта Российской Федерации')
    entry1_SvCenterAdr = ttk.Entry(AdrRazmObkt_window, width=50)
    entry1_SvCenterAdr.grid(row=1, column=1, padx=5, pady=5)

    label2_SvCenterAdr = ttk.Label(AdrRazmObkt_window, text='Индекс*')
    label2_SvCenterAdr.grid(row=2, column=0, padx=5, pady=5)
    CreateToolTip(label2_SvCenterAdr, text='Почтовый индекс')
    entry2_SvCenterAdr = ttk.Entry(AdrRazmObkt_window, width=50)
    entry2_SvCenterAdr.grid(row=2, column=1, padx=5, pady=5)

    label3_SvCenterAdr = ttk.Label(AdrRazmObkt_window, text='НаимГор*')
    label3_SvCenterAdr.grid(row=3, column=0, padx=5, pady=5)
    CreateToolTip(label3_SvCenterAdr, text='Наименование населенного пункта')
    entry3_SvCenterAdr = ttk.Entry(AdrRazmObkt_window, width=50)
    entry3_SvCenterAdr.grid(row=3, column=1, padx=5, pady=5)

    label4_SvCenterAdr = ttk.Label(AdrRazmObkt_window, text='Адрес')
    label4_SvCenterAdr.grid(row=4, column=0, padx=5, pady=5)
    CreateToolTip(label4_SvCenterAdr, text='Адрес')
    entry4_SvCenterAdr = ttk.Entry(AdrRazmObkt_window, width=50)
    entry4_SvCenterAdr.grid(row=4, column=1, padx=5, pady=5)

    label10_SvCenterAdr = ttk.Label(AdrRazmObkt_window, text='* - необязательные данные')
    label10_SvCenterAdr.grid(row=5, column=0, padx=5, pady=5)

    btn1_SvCenterAdr = ttk.Button(AdrRazmObkt_window, text="Сохранить данные",
                                  command=lambda j4=j, jj4=jj, Adr_i=Doc_ii: save_data_svcenteradrobkt(j4, jj4, Adr_i, entry0_SvCenterAdr.get(),
                                                                        entry1_SvCenterAdr.get(),
                                                                        entry2_SvCenterAdr.get(),
                                                                        entry3_SvCenterAdr.get(),
                                                                        entry4_SvCenterAdr.get()))
    btn1_SvCenterAdr.grid(row=6, column=1, padx=5, pady=5)

    return


def save_data_svcenteradrobkt(j, jj, Adr_i, codreg, naimreg, index, naimgor, adres):
    global elementss

    var_name = "AdrRazmObkt" + str(jj) + "." + str(j) + str(Adr_i)
    elementss[var_name] = etree.SubElement(elementss["SvAdrRazm" + str(jj) + "." + str(j)], "АдрРазмОбкт")

    var_name = "CodRegion" + str(jj) + str(j) + str(Adr_i)
    elementss[var_name] = etree.SubElement(elementss["AdrRazmObkt" + str(jj) + "." + str(j) + str(Adr_i)], "КодРегион")
    elementss[var_name].text = codreg

    var_name = "NaimRegion" + str(jj) + str(j) + str(Adr_i)
    elementss[var_name] = etree.SubElement(elementss["AdrRazmObkt" + str(jj) + "." + str(j) + str(Adr_i)],
                                           "НаимРегион")
    elementss[var_name].text = naimreg

    if len(index) > 0:
        var_name = "Index" + str(jj) + str(j) + str(Adr_i)
        elementss[var_name] = etree.SubElement(elementss["AdrRazmObkt" + str(jj) + "." + str(j) + str(Adr_i)], "Индекс")
        elementss[var_name].text = index

    if len(naimgor) > 0:
        var_name = "NaimGor" + str(jj) + str(j) + str(Adr_i)
        elementss[var_name] = etree.SubElement(elementss["AdrRazmObkt" + str(jj) + "." + str(j) + str(Adr_i)], "НаимГор")
        elementss[var_name].text = naimgor

    var_name = "Adress" + str(jj) + str(j) + str(Adr_i)
    elementss[var_name] = etree.SubElement(elementss["AdrRazmObkt" + str(jj) + "." + str(j) + str(Adr_i)], "Адрес")
    elementss[var_name].text = adres

    # print(etree.tostring(SvCentrAdr, encoding='unicode', method='xml'))
    # Если валидация прошла успешно, сохраняем данные
    # save_data_to_xml(ogrn_value, inn_value)
    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global AdrRazmObkt_window
    AdrRazmObkt_window.destroy()
    return


def SvZOULSeti_button_clicked(string, jj):
    global SvZOULSeti_window
    SvZOULSeti_window = Tk()
    SvZOULSeti_window.title("СвЗОЮЛСети" + ". " + "ЕдЗО " + str(jj))
    SvZOULSeti_window.geometry("900x600")

    btn1 = ttk.Button(SvZOULSeti_window, text="IPv4*",
                      command=lambda jj3=jj: ipv4_button_clicked(jj3))
    btn1.grid(row=0, column=1, padx=5, pady=5)
    CreateToolTip(btn1, text='Внешний маршрутизируемый IPv4-адрес')

    btn1 = ttk.Button(SvZOULSeti_window, text="IPv6*",
                      command=lambda jj4=jj: ipv6_button_clicked(jj4))
    btn1.grid(row=1, column=1, padx=5, pady=5)
    CreateToolTip(btn1, text='Внешний маршрутизируемый IPv6-адрес')

    btn1 = ttk.Button(SvZOULSeti_window, text="FQDN*",
                      command=lambda jj5=jj: fqdn_button_clicked(jj5))
    btn1.grid(row=2, column=1, padx=5, pady=5)
    CreateToolTip(btn1, text='Полное наименование доменного имени')

    btn1 = ttk.Button(SvZOULSeti_window, text="AS*",
                      command=lambda jj6=jj: as_button_clicked(jj6))
    btn1.grid(row=3, column=1, padx=5, pady=5)
    CreateToolTip(btn1, text='Описание автономной системы')

    label10_SvCenterAdr = ttk.Label(SvZOULSeti_window, text='* - необязательные данные')
    label10_SvCenterAdr.grid(row=4, column=1, padx=5, pady=5)
    return


def ipv4_button_clicked(jj):
    global ipv4_window
    ipv4_window = Tk()
    ipv4_window.title("IPv4 " + "ЕдЗО " + str(jj))
    ipv4_window.geometry("900x600")
    global btn110_elems
    btn110_elems = {}
    global ipv4_i
    ipv4_i = 0
    btn1 = ttk.Button(ipv4_window, text="Добавить IPv4",
                      command=lambda jj1=jj: add_ipv4(jj1))
    btn1.grid(row=0, column=0, padx=5, pady=5)

    btn1 = ttk.Button(ipv4_window, text="Удалить IPv4",
                      command=lambda jj2=jj: del_ipv4(jj2))
    btn1.grid(row=0, column=1, padx=5, pady=5)


    label3 = ttk.Label(ipv4_window, text='IPv4-адреса:')
    label3.grid(row=1, column=0, padx=5, pady=5)

    btn1_SvFunk = ttk.Button(ipv4_window, text="Сохранить данные",
                             command=lambda jj4=jj: save_ipv4_inxml(jj4))
    btn1_SvFunk.grid(row=4, column=2, padx=5, pady=5)

    return


def add_ipv4(jj):
    global ipv4_window
    global btn110_elems
    global ipv4_i
    ipv4_i = ipv4_i + 1
    btn110_name = "btn110_" + str(jj) + str(ipv4_i)

    btn110_elems[btn110_name] = ttk.Entry(ipv4_window, width=50)
    btn110_elems[btn110_name].grid(row=ipv4_i, column=1, padx=5, pady=5)

    return


def del_ipv4(jj):
    global ipv4_window
    global btn110_elems
    global ipv4_i
    if ipv4_i > 0:
        btn110_name = "btn110_" + str(jj) + str(ipv4_i)
        btn110_elems[btn110_name].destroy()
        del btn110_elems[btn110_name]
        ipv4_i = ipv4_i - 1
    return


def save_ipv4_inxml(jj):
    global ipv4_i
    global btn110_elems
    global elements
    i = 1

    while i <= ipv4_i:
        btn110_name = "btn110_" + str(jj) + str(i)
        var_name = "IPv4" + str(jj) + "." + str(i)
        elements[var_name] = etree.SubElement(elements["SvZOULSeti" + str(jj)], "IPv4")
        elements[var_name].text = btn110_elems[btn110_name].get()
        i = i + 1

    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global ipv4_window
    ipv4_window.destroy()


def ipv6_button_clicked(jj):
    global ipv6_window
    ipv6_window = Tk()
    ipv6_window.title("IPv6 " + "ЕдЗО " + str(jj))
    ipv6_window.geometry("900x600")
    global btn120_elems
    btn120_elems = {}
    global ipv6_i
    ipv6_i = 0
    btn1 = ttk.Button(ipv6_window, text="Добавить IPv6",
                      command=lambda jj1=jj: add_ipv6(jj1))
    btn1.grid(row=0, column=0, padx=5, pady=5)

    btn1 = ttk.Button(ipv6_window, text="Удалить IPv6",
                      command=lambda jj2=jj: del_ipv6(jj2))
    btn1.grid(row=0, column=1, padx=5, pady=5)


    label3 = ttk.Label(ipv6_window, text='IPv6-адреса:')
    label3.grid(row=1, column=0, padx=5, pady=5)

    btn1_SvFunk = ttk.Button(ipv6_window, text="Сохранить данные",
                             command=lambda jj4=jj: save_ipv6_inxml(jj4))
    btn1_SvFunk.grid(row=4, column=2, padx=5, pady=5)

    return


def add_ipv6(jj):
    global ipv6_window
    global btn120_elems
    global ipv6_i
    ipv6_i = ipv6_i + 1
    btn120_name = "btn120_" + str(jj) + str(ipv6_i)

    btn120_elems[btn120_name] = ttk.Entry(ipv6_window, width=50)
    btn120_elems[btn120_name].grid(row=ipv6_i, column=1, padx=5, pady=5)

    return


def del_ipv6(jj):
    global ipv6_window
    global btn120_elems
    global ipv6_i
    if ipv6_i > 0:
        btn120_name = "btn120_" + str(jj) + str(ipv6_i)
        btn120_elems[btn120_name].destroy()
        del btn120_elems[btn120_name]
        ipv6_i = ipv6_i - 1
    return


def save_ipv6_inxml(jj):
    global ipv6_i
    global btn120_elems
    global elements
    i = 1

    while i <= ipv6_i:
        btn120_name = "btn120_" + str(jj) + str(i)
        var_name = "IPv6" + str(jj) + "." + str(i)
        elements[var_name] = etree.SubElement(elements["SvZOULSeti" + str(jj)], "IPv6")
        elements[var_name].text = btn120_elems[btn120_name].get()
        i = i + 1

    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global ipv6_window
    ipv6_window.destroy()


def fqdn_button_clicked(jj):
    global fqdn_window
    fqdn_window = Tk()
    fqdn_window.title("FQDN " + "ЕдЗО " + str(jj))
    fqdn_window.geometry("900x600")
    global btn130_elems
    btn130_elems = {}
    global fqdn_i
    fqdn_i = 0
    btn1 = ttk.Button(fqdn_window, text="Добавить FQDN",
                      command=lambda jj1=jj: add_fqdn(jj1))
    btn1.grid(row=0, column=0, padx=5, pady=5)

    btn1 = ttk.Button(fqdn_window, text="Удалить FQDN",
                      command=lambda jj2=jj: del_fqdn(jj2))
    btn1.grid(row=0, column=1, padx=5, pady=5)


    label3 = ttk.Label(fqdn_window, text='Полное наименование доменного имени:')
    label3.grid(row=1, column=0, padx=5, pady=5)

    btn1_SvFunk = ttk.Button(fqdn_window, text="Сохранить данные",
                             command=lambda jj4=jj: save_fqdn_inxml(jj4))
    btn1_SvFunk.grid(row=4, column=2, padx=5, pady=5)

    return


def add_fqdn(jj):
    global fqdn_window
    global btn130_elems
    global fqdn_i
    fqdn_i = fqdn_i + 1
    btn130_name = "btn130_" + str(jj) + str(fqdn_i)

    btn130_elems[btn130_name] = ttk.Entry(fqdn_window, width=50)
    btn130_elems[btn130_name].grid(row=fqdn_i, column=1, padx=5, pady=5)

    return


def del_fqdn(jj):
    global fqdn_window
    global btn130_elems
    global fqdn_i
    if fqdn_i > 0:
        btn130_name = "btn130_" + str(jj) + str(fqdn_i)
        btn130_elems[btn130_name].destroy()
        del btn130_elems[btn130_name]
        fqdn_i = fqdn_i - 1
    return


def save_fqdn_inxml(jj):
    global fqdn_i
    global btn130_elems
    global elements
    i = 1

    while i <= fqdn_i:
        btn130_name = "btn130_" + str(jj) + str(i)
        var_name = "FQDN" + str(jj) + "." + str(i)
        elements[var_name] = etree.SubElement(elements["SvZOULSeti" + str(jj)], "FQDN")
        elements[var_name].text = btn130_elems[btn130_name].get()
        i = i + 1

    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global fqdn_window
    fqdn_window.destroy()


def as_button_clicked(jj):
    global as_window
    as_window = Tk()
    as_window.title("AS " + "ЕдЗО " + str(jj))
    as_window.geometry("900x600")
    global btn140_elems
    btn140_elems = {}
    global as_i
    as_i = 0
    btn1 = ttk.Button(as_window, text="Добавить AS",
                      command=lambda jj1=jj: add_as(jj1))
    btn1.grid(row=0, column=0, padx=5, pady=5)

    btn1 = ttk.Button(as_window, text="Удалить AS",
                      command=lambda jj2=jj: del_as(jj2))
    btn1.grid(row=0, column=1, padx=5, pady=5)


    label3 = ttk.Label(as_window, text='Описание автономной системы:')
    label3.grid(row=1, column=0, padx=5, pady=5)

    btn1_SvFunk = ttk.Button(as_window, text="Сохранить данные",
                             command=lambda jj4=jj: save_as_inxml(jj4))
    btn1_SvFunk.grid(row=4, column=2, padx=5, pady=5)

    return


def add_as(jj):
    global as_window
    global btn140_elems
    global as_i
    as_i = as_i + 1
    btn140_name = "btn140_" + str(jj) + str(as_i)

    btn140_elems[btn140_name] = ttk.Entry(as_window, width=50)
    btn140_elems[btn140_name].grid(row=as_i, column=1, padx=5, pady=5)
    return


def del_as(jj):
    global as_window
    global btn140_elems
    global as_i
    if as_i > 0:
        btn140_name = "btn140_" + str(jj) + str(as_i)
        btn140_elems[btn140_name].destroy()
        del btn140_elems[btn140_name]
        as_i = as_i - 1
    return


def save_as_inxml(jj):
    global as_i
    global btn140_elems
    global elements
    i = 1

    while i <= as_i:
        btn140_name = "btn140_" + str(jj) + str(i)
        var_name = "AS" + str(jj) + "." + str(i)
        elements[var_name] = etree.SubElement(elements["SvZOULSeti" + str(jj)], "AS")
        elements[var_name].text = btn140_elems[btn140_name].get()
        i = i + 1

    messagebox.showinfo("Успешно", "Данные успешно сохранены")
    global as_window
    as_window.destroy()


# Создание корневого элемента
SvCentrGS = etree.Element("СвЦентрГС")
SvCentrGS.set("ДатаФорм", "value")
SvCentrGS.set("НаимЦентр", "value")
SvCentrGS.set("КлассЦентр", "value")
SvCentrGS.set("СхемВерс", "00")

# Добавление дочерних элементов
SvULTip = etree.SubElement(SvCentrGS, "СвЮЛ")
SvULTip.set("ОРГН", "value")  # required
SvULTip.set("ИНН", "value")  # required
SvULTip.set("КПП", "value")  # required
SvULTip.set("НаимЮЛПолн", "value")  # required
SvULTip.set("НаимЮЛСокр", "value")
SvULTip.set("Тип", "value")  # required
SvULTip.set("Сайт", "value")
SvULTip.set("ОКВЭД", "value")  # required
SvULTip.set("ОКОГУ", "value")
SvULTip.set("ОКОПФ", "value")

SvCentrAdr = etree.SubElement(SvCentrGS, "СвЦентрАдр")
CodRegion = etree.SubElement(SvCentrAdr, "КодРегион")
NaimRegion = etree.SubElement(SvCentrAdr, "НаимРегион")
Indeks = etree.SubElement(SvCentrAdr, "Индекс")  # Необязательно
NaimGor = etree.SubElement(SvCentrAdr, "НаимГор")  # Необязательно
Adres = etree.SubElement(SvCentrAdr, "Адрес")

# btn4 = {}
SvCenterCont_Pod = {}
FIO_Pod = {}
Podrazd_Pod = {}
Dolzhn_Pod = {}
RabTel_Pod = {}
MobTel_Pod = {}
ElPoch_Pod = {}
SvCentrCont = etree.SubElement(SvCentrGS, "СвЦентрКонт")  # Одно или несколько вхождений
FIO = etree.SubElement(SvCentrCont, "ФИО")
Podrazd = etree.SubElement(SvCentrCont, "Подразд")  # Необязательно
Dolzhn = etree.SubElement(SvCentrCont, "Должн")  # Необязательно
RabTel = etree.SubElement(SvCentrCont, "РабТел")
MobTel = etree.SubElement(SvCentrCont, "МобТел")  # Необязательно
ElPoch = etree.SubElement(SvCentrCont, "ЭлПоч")  # Необязательно

SvZonaOtv = etree.SubElement(SvCentrGS, "СвЗонаОтв")

# Создание XML-дерева
tree = etree.ElementTree(SvCentrGS)

# Вывод XML-документа в консоль
# print(etree.tostring(SvCentrGS, encoding='UTF-8', pretty_print=True).decode())


root = Tk()  # создаем корневой объект - окно
root.title("GosSOPKA XML Parser")  # устанавливаем заголовок окна
root.geometry("900x600")  # устанавливаем размеры окна

# Кнопка для элемента СвЦентрГС
btn1 = ttk.Button(text="СвЮЛ", command=lambda: SvUL_button_clicked("СвЮЛ", 0))
btn1.grid(row=0, column=1, padx=5, pady=5)
CreateToolTip(btn1, text='Сведения о юридическом лице, на мощностях которого организован центр ГосСОПКА')

btn2 = ttk.Button(text="СвЦентрАдр", command=lambda: SvCenterAdr_button_clicked("СвЦентрАдр"))
btn2.grid(row=1, column=1, padx=5, pady=5)
CreateToolTip(btn2,
              text='Сведения о почтовом адресе юридического лица, на мощностях которого организован центр ГосСОПКА')

global index_row
index_row = 2
btn3 = ttk.Button(text='СвЦентрКонт', command=lambda: SvCenterCont_button_clicked("СвЦентрКонт", 0, 0))
btn3.grid(row=index_row, column=1, padx=5, pady=5)
CreateToolTip(btn3, text='Сведения о контактном лице центра ГосСОПКА по вопросам взаимодействия')

btn5 = ttk.Button(text='+СвЦентрКонт', command=lambda: PlusSvCenterCont_button_clicked("+СвЦентрКонт"))
btn5.grid(row=index_row + 1, column=2, padx=5, pady=5)
CreateToolTip(btn5, text='Добавить дополнительное контактное лицо центра ГосСОПКА')

btn6 = ttk.Button(text='-СвЦентрКонт', command=lambda: MinusSvCenterCont_button_clicked("-СвЦентрКонт"))
btn6.grid(row=index_row + 1, column=3, padx=5, pady=5)
CreateToolTip(btn6, text='Убрать дополнительное контактное лицо центра ГосСОПКА')

btn4 = ttk.Button(text='СвЗонаОтв', command=lambda: SvZonaOtv_button_clicked("СвЗонаОтв"))
btn4.grid(row=index_row + 2, column=1, padx=5, pady=5)
CreateToolTip(btn4, text='Единица зоны ответственности центра ГосСОПКА')

label1 = ttk.Label(text='ДатаФорм: YYYY-MM-DD')
label1.grid(row=index_row + 3, column=0, padx=5, pady=5)
CreateToolTip(label1, text='Дата формирования XML документа')
entry1000 = ttk.Entry()
entry1000.grid(row=index_row + 3, column=1, padx=5, pady=5)

label2 = ttk.Label(text='НаимЦентр')
label2.grid(row=index_row + 4, column=0, padx=5, pady=5)
CreateToolTip(label2, text='Наименование центра ГосСОПКА')
entry2000 = ttk.Entry(width=50)
entry2000.grid(row=index_row + 4, column=1, padx=5, pady=5)

klass_center = ['А', 'Б', 'В']
label3 = ttk.Label(text='КлассЦентр')
label3.grid(row=index_row + 5, column=0, padx=5, pady=5)
CreateToolTip(label3, text='Класс центра ГосСОПКА')
combobox1 = ttk.Combobox(values=klass_center, state='readonly')
combobox1.grid(row=index_row + 5, column=1, padx=5, pady=5)
combobox1.bind("<<ComboboxSelected>>", selected1)

scheme_versions = ['00']
label4 = ttk.Label(text='СхемВерс')
index_row = index_row + 1
label4.grid(row=index_row + 6, column=0, padx=5, pady=5)
CreateToolTip(label4, text='Версия схемы')
combobox2 = ttk.Combobox(values=scheme_versions, state='readonly')
combobox2.grid(row=index_row + 6, column=1, padx=5, pady=5)
combobox2.bind("<<ComboboxSelected>>", selected2)

# Добавляем кнопки для независимых complexType
# self.add_independent_complex_type_buttons(crollable_frame)

# Кнопка "Save XML"
btn_save_xml = ttk.Button(text="Generate XML", command=generate_xml)
btn_save_xml.grid(row=0, column=2, padx=5, pady=5)

root.mainloop()
