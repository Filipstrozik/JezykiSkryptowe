import subprocess
import sys

if __name__ == '__main__':
    continent = ''
    year = ''
    nLines = 1

    for param in sys.argv:
        if param.find("--continent=") != -1:
            continent = param.replace("--continent=", "")
        elif param.find("--lines=") != -1:
            nLines = int(param.replace("--lines=", ""))
        elif param.find("--year=") != -1:
            year = param.replace("--year=", "")

    output_continent = ''
    try:
        output_continent = subprocess.check_output(
            f'java process --select={continent} < covid.tsv ',
            shell=True,
            universal_newlines=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 2:
            print('error with input')
            sys.exit(2)
        if e.returncode == 1:
            print('error with continent')
            sys.exit(1)

    output_countries = ''
    try:
        output_countries = subprocess.check_output(
            f'java process --delimiter="\t" --project=7',
            shell=True,
            text=True,
            universal_newlines=True,
            input=output_continent
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 2:
            print('error with input')
            sys.exit(2)
        if e.returncode == 1:
            print('error with month')
            sys.exit(1)

    countriesSplitted = output_countries.split('\n')
    countriesDict = {}

    for country in countriesSplitted:
        if country.istitle():
            country = country[0:-2]
            countriesDict[country] = 0

    for coun in countriesDict.keys():
        output_for_each_country = subprocess.check_output(
            f'java process --delimiter="\t" --project=1,5,7 --select={coun}'
            f'| java process --delimiter"\t" --select={year}'
            f'| java process --delimiter="\t\t" --project=2 '
            f'| java Aggregate /avg',
            shell=True,
            text=True,
            universal_newlines=True,
            input=output_continent
        )
        countriesDict[coun] = float(output_for_each_country)
    countriesList = sorted(countriesDict.items(), key=lambda x: x[1], reverse=True)

    result = ''

    for elem in countriesList:
        result += str(elem[0]) + " " + str(elem[1]) + "\n"

    subprocess.run(f'java Head --lines={nLines}',
                   text=True,
                   input=result)