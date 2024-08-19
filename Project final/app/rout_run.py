from flask import Flask, render_template, request, send_file,jsonify
from Germany.versteigerungskalender import verstei
from Germany.insolvenzbekanntmachungen import Insolvenzbekanntmachungen
from Germany.unternehmensregister import unternehmensregister
from Germany.dealone import deal
from waitress import serve
from tools import save_to_excel,convert_to_df,convert_to_df,reverse_date_format,translate_to_en,reverse_date_format1
from Denmark.statstidendeProffAuktioner import statstidendeProffAuktioner
from Denmark.proff import proff
from Denmark.auktioner import auktioner
from Denmark.statstidende import statstidende
from UnitedKingdom.gazetteuk import GazetteUK

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        site = request.form.get('site')
        

        if site == 'versteigerungskalender':
            sector = request.form.get('sector')
            keywords = request.form.get('keywords')
            try:
                data = verstei(keywords)
            except:
                return render_template("error.html")
            filename = "verstei_data.xlsx"
            file = save_to_excel(data, filename)
            return render_template('down.html', filename=file)
        
        if site == "Insolvenzbekanntmachungen":
            keywords = request.form.get('keywords')
            dateStart = reverse_date_format(request.form.get('dateStart'))
            dateEnd = reverse_date_format(request.form.get('dateEnd'))
            selligent = True if request.form.get('checking') else False
            trans = True if request.form.get('translation') else False
            print(trans)
            try:
                data = Insolvenzbekanntmachungen(keywords,dateStart,dateEnd,selligent,trans)
            except:
                render_template("error.html")
            filename = "insolv_data.xlsx"
            file = save_to_excel(data, filename)
            return render_template('down.html', filename=file)

        if site == "unternehmensregister":
            dateStart = reverse_date_format(request.form.get('dateStart'))
            dateEnd = reverse_date_format(request.form.get('dateEnd'))
            try:
                data = unternehmensregister(dateStart,dateEnd)
            except:
                return render_template('error.html')
            filename = "unter_data.xlsx"
            file = save_to_excel(data, filename)
            return render_template('down.html', filename=file)
        
        if site == "dealone":
            keywords = request.form.get('keywords')
            
            try:
                data = deal(keywords)
            except:
                return render_template("error.html")
            
            df = convert_to_df(data)
            filename = "DealOne_data.xlsx"
            file = save_to_excel(data, filename)
        
            return render_template('down.html', filename=file)
        if site=="statstidende-proff-auktioner-OC":
            dateStart = reverse_date_format1(request.form.get('dateStart'))
            dateEnd = reverse_date_format1(request.form.get('dateEnd'))
            selligent = True if request.form.get('checking') else False
            trans = True if request.form.get('translation') else False
            try:
                data = statstidendeProffAuktioner(dateStart,dateEnd,selligent,trans)
            except:
                return render_template('error.html')
            filename = "statstidende-proff-auktioner_data.xlsx"
            file = save_to_excel(data, filename)
            return render_template('down.html', filename=file)
        
        if site=="statstidende":
            dateStart = reverse_date_format1(request.form.get('dateStart'))
            
            dateEnd = reverse_date_format1(request.form.get('dateEnd'))

            print(dateStart)
            print(dateEnd)
            try:
                data = statstidende(dateStart,dateEnd)
            except:
                return render_template('error.html')
            filename = "statstidende.xlsx"

            file = save_to_excel(data, filename)
            return render_template('down.html', filename=file)
            
        if site=="proff":
            text = request.form.get('Keywords')
            try:
                address,domaine,status = proff(text)
            except:
                return render_template('error.html')
        
            data = {
            'address': address,
            'domaine': translate_to_en(domaine),
            'status': translate_to_en(status)
            }
            return render_template('popup.html',data=data)
        if site=='auktioner':
            text = request.form.get('Keywords')
            try:
                cleaned_texts,a,b = auktioner(text)
                print(cleaned_texts)
                
            except:
                return render_template('error.html')
            # Assuming cleaned_texts is a list of dictionaries and you want to find the first dictionary with a matching key
            def lis_to_text(list):
                text =""
                for value in list:
                    text += value + ", "
                return text
            data = {
                'Curator': lis_to_text(cleaned_texts)
            }
        

            return render_template("popup.html",data=data)

        if site == "GazetteUK":
            dateStart = reverse_date_format(request.form.get('dateStart'))
            dateEnd = reverse_date_format(request.form.get('dateEnd'))
            
            data = GazetteUK(dateStart,dateEnd)
            print(data)
            
            filename = "GazetteUK_data.xlsx"
            file = save_to_excel(data, filename)
            return render_template('down.html', filename=file)

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    path = filename  # Assuming the file is in the current working directory
    return send_file(path, as_attachment=True)

#waitress  
"""if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8181)
"""

#run
if __name__ == '__main__':
    app.run(debug=True)