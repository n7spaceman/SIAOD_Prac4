from tkinter import *
from tkinter.ttk import *
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go


# https://ru.flightaware.com/live/flight/GZP9621/history


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def draw_graph():
    layout = go.Layout(
        title='',
    )

    #data = go.Scatter(
     #   x=latitudes,
      #  y=longitudes,
       # mode='lines',
        #name='loool'
    #)

    data = go.Scattermapbox(
        mode="lines",
        lon=longitudes,
        lat=latitudes,
        marker={'size': 15}
    )

    data1 = go.Scattermapbox(
        mode="lines",
        lon=[0],
        lat=[0],
        marker={'size': 1}
    )

    fig = go.Figure(layout=layout, data=data)

    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            #'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1})

    fig.show()


def get_url(flight_num):
    url = 'https://ru.flightaware.com/live/flight/' + flight_num + '/history'
    return url


'''
def get_dates_from_history_url(history_url):
    source = requests.get(history_url)
    main_text = source.text
    soup = BeautifulSoup(main_text, 'lxml')

    tags_td_test = soup.find_all('td', attrs={'class': 'nowrap'})
    tags_a = []

    for tag in tags_td_test:
        tags_a.append(tag.find('a').text)
        date_array.append(tag.find('a').attrs['href'][29:37])

    return tags_a
'''


def fill_dates_array(history_url):
    source = requests.get(history_url)
    main_text = source.text
    soup = BeautifulSoup(main_text, 'lxml')

    tags_td_test = soup.find_all('td', attrs={'class': 'nowrap'})

    for tag in tags_td_test:
        dates_array.append(tag.find('a').attrs['href'][29:37])
        hrefs_in_tags.append(tag.find('a').attrs['href'])


def btn2_clicked():
    idx = times.index(cmb_time_select.get())
    text_for_lbl_t_s = 'Широта: '+str(latitudes[idx])+' Долгота: '+str(longitudes[idx])
    lbl_time_select.configure(text=text_for_lbl_t_s)


def btn1_clicked():
    index_of_date = normal_dates_array.index(cmb_date_select.get())
    date_for_flight_url = dates_array[index_of_date]
    flight_url = 'https://ru.flightaware.com'+hrefs_in_tags[index_of_date]+'/tracklog'
    lbl_link.configure(text=flight_url)

    source = requests.get(flight_url)
    main_text = source.text
    soup = BeautifulSoup(main_text, 'lxml')

    # spans = soup.find_all('span', {'class': 'show-for-medium-up'} or {'class': 'hide-for-medium-up'})
    trs = soup.find_all('tr', {'class': 'smallrow1'} or {'class': 'smallrow2'})

    '''
    for i in range(10, len(spans), 10):
        # times.append(spans[i].text[3:])
        if is_digit(spans[i+1].text) and is_digit(spans[i+2].text):
            latitudes.append(float(spans[i + 1].text))
            longitudes.append(float(spans[i + 2].text))
    '''

    for tr in trs:
        tds = tr.find_all('td')
        if is_digit(tds[1].find('span').text) and is_digit(tds[2].find('span').text):
            times.append(tds[0].find('span').text[3:])
            latitudes.append(float(tds[1].find('span').text))
            longitudes.append(float(tds[2].find('span').text))

    cmb_time_select['values'] = times

    lbl_4 = Label(window, text='Выберите время полета:')
    lbl_4.grid(row=4, column=0, columnspan=2)

    cmb_time_select.grid(row=5, column=0)
    btn_time_select.grid(row=5, column=1)
    lbl_time_select.grid(row=6, column=0, columnspan=2)

    # print(soup.prettify())
    print(flight_url[:-9])
    print(times)
    print(latitudes)
    print(longitudes)
    draw_graph()


def btn_clicked():
    history_url = get_url(cmb_flight_select.get())
    lbl_link.configure(text=history_url)
    # dates = [1, 2, 3]
    # dates = get_dates_from_history_url(history_url)
    fill_dates_array(history_url)

    lbl_3 = Label(window, text='Выберите дату полета:')
    lbl_3.grid(row=2, column=0, columnspan=2)

    cmb_date_select.grid(row=3, column=0)

    btn1 = Button(window, text='Click', command=btn1_clicked)
    btn1.grid(row=3, column=1)

    for i in dates_array:
        normal_dates_array.append(i[6:] + '.' + i[4:6] + '.' + i[:4])

    cmb_date_select['values'] = normal_dates_array

    # flight_page = get_flight_page(cmb1.get())


window = Tk()
window.title("Lab4")
window.geometry('800x150')

dates_array = []
normal_dates_array = []
hrefs_in_tags = []

latitudes = []
longitudes = []
times = []

lbl_1 = Label(window, text='Выберите рейс:')
lbl_1.grid(row=0, column=0, columnspan=2)

cmb_date_select = Combobox(window)
cmb_flight_select = Combobox(window)
cmb_flight_select.grid(row=1, column=0)
cmb_flight_select['values'] = ('GZP9621', 'CHB6212', 'CDG4700', 'N3198W', 'SKW4276', 'N693TF')

lbl_2 = Label(window, text='Ссылка на страницу, с которой производится работа:')
lbl_2.grid(row=0, column=2, columnspan=99)
lbl_link = Label(window, text='')
lbl_link.grid(row=1, column=2)

btn_flight_select = Button(window, text='Click', command=btn_clicked)
btn_flight_select.grid(row=1, column=1)

cmb_time_select = Combobox(window)
btn_time_select = Button(window, text='Click', command=btn2_clicked)
lbl_time_select = Label(window, text='')

window.mainloop()
