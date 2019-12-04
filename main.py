from db_part import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/flights', methods=['GET', 'POST'])
def flights():
    return render_template("flights.html")


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    linie = pokaz_linie()
    lotniska = pokaz_lotniska()
    return render_template("schedule.html", linie=linie, lotniska=lotniska)


@app.route('/lines', methods=['GET', 'POST'])
def lines():
    notification = None
    if request.method == 'POST':
        req = request.values.to_dict()
        if 'new' in req:
            notification = dodaj_linie(req['nazwa'], req['kraj'])
        if 'remove' in req:
            notification = usun_linie(nazwa=req['remove'])
    linie = pokaz_linie()
    kraje = get_countries_list()
    return render_template("lines.html", linie=linie, notification=notification, kraje=kraje)


@app.route('/lines/<line>', methods=['GET', 'POST'])
def line_name(line):
    linia = pokaz_linie(line)
    if not linia:
        abort(404)
    notification = None
    if request.method == 'POST':
        req = request.values.to_dict()
        if 'new-samolot' in req:
            notification = dodaj_samolot(nr_boczny=req['nr_boczny'], marka=req['marka'], model=req['model'],
                                         linia_nazwa=linia.nazwa, pojemnosc=req['pojemnosc'],
                                         zasieg=req['zasieg'])
        elif 'remove-samolot' in req:
            notification = usun_samolot(nr_boczny=req['remove'])
        elif 'new-pilot' in req:
            notification = dodaj_pilota(imie=req['imie'], nazwisko=req['nazwisko'], linia_nazwa=linia.nazwa)
    samoloty = pokaz_samoloty(linia=line)
    piloci = pokaz_pilotow(linia=line)
    return render_template("line.html", linia=linia, samoloty=samoloty, piloci=piloci, notification=notification)


@app.route('/airports', methods=['GET', 'POST'])
def airports():
    notification = None
    if request.method == 'POST':
        req = request.values.to_dict()
        if 'new' in req:
            notification = dodaj_lotnisko(kod=req['code'], kraj=req['country'],
                                          miasto=req['city'], m_na_mapie=req['map'], strefa_czasowa=req['timezone'])
        elif 'edit' in req:
            notification = zmodyfikuj_lotnisko(kod=req['edit'], nowy_kod=req['code'], kraj=req['country'],
                                               miasto=req['city'], m_na_mapie=req['map'],
                                               strefa_czasowa=req['timezone'])
        elif 'remove' in req:
            notification = usun_lotnisko(kod=req['remove'])
    kraje = get_countries_list()
    lotniska = pokaz_lotniska()
    return render_template('airports.html', kraje=kraje, notification=notification, lotniska=lotniska)


@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
