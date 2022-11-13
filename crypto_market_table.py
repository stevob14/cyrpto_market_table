import requests

def cg_api():
    api = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    try:
        data = requests.get(api,timeout=10).json()
        return data
    except requests.exceptions.RequestException:
        return False
    except (ValueError):
        return False

def market_table():
    data = cg_api()
    if data:
        output = "<table id='cryptotable' class='row-border compact'><thead><tr><th>#</th><th>Name</th><th>Market Cap</th><th>Price</th><th>Volume (24h)</th><th>Circulating Supply</th><th>Change (24h)</th></tr></thead>"
        for x in data:
            try:
                id = x['id']
                rank = str(x['market_cap_rank'])
                name = x['name']
                symbol = x['symbol']
                market_cap = comma_format(x['market_cap'])
                price = x['current_price']
                if price < .1:
                    price = f'{price:.8f}'
                else:
                    price = comma_format(price)
                volume = comma_format(x['total_volume'])
                circulating_supply=comma_format(x['circulating_supply'])
                change_24 = x['price_change_percentage_24h']
                output+= "<tr><td>" + rank + "</td><td><a href="+id+" id=searchfromtable name=" + id + "|" + symbol + ">" + name + "</a></td>" + "<td>$" + market_cap + "</td>" + "<td><span style='color:#58A6FF'>$" + price + "</span></td>"+"<td>$" + volume + "</td>"+"<td>" + circulating_supply + " " + symbol + "</td>"
                change_24h = dec_format(change_24)
                output+="<td>" + color_change_percent(change_24h) + "</td></tr>"
            except (IndexError, KeyError, TypeError, ValueError):
                pass
        output+= "</table>"
    else:
        output= "There was an error retrieving data from the api :/ Try refreshing the page."
    return output

def comma_format(value):
    try:
        change = "{:,}".format(float(value))
    except(TypeError, ValueError):
        change = "N/A"
    return change

def dec_format(value):
    try:
        change = "{0:.2f}".format(float(value))
    except(TypeError):
        change = "N/A"
    return change

def color_change_percent(change):
    output = ""
    try:
        if float(change) > 0:
            output+="<span style='color:#00C853'>" + change + "%</span>"
        elif float(change) < 0:
            output+="<span style='color:#ff0000'>" + change + "%</span>"
        else:
            output+= change
    except (TypeError, ValueError):
        output+="N/A"
    return output

test = market_table()
print(test)
