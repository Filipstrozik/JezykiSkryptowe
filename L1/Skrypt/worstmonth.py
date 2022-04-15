import subprocess
import sys

if __name__ == '__main__':

    country = ''
    sortmode = True
    nLines = 1
    year = 2020

    for param in sys.argv:
        if param.find("--country=") != -1:
            country = param.replace("--country=", "")
        elif param.find("--best") != -1:
            sortmode = False
        elif param.find("--worst") != -1:
            sortmode = True
        elif param.find("--lines=") != -1:
            nLines = int(param.replace("--lines=", ""))
        elif param.find("--year=") != -1:
            year = param.replace("--year=", "")

    output_country = ''
    try:
        output_country = subprocess.check_output(
            f'java process '
            f'--select={country} < covid.tsv '
            f'| java process --delimiter="\t" --separator="\t" --project=1,6,7'
            f'| java process --select={year}',
            shell=True,
            universal_newlines=True,
            text=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 2:
            print('error with input')
            sys.exit(2)
        if e.returncode == 1:
            print('error with selecting')
            sys.exit(1)

    dates = subprocess.check_output(f'java process --delimiter="\t" --separator="\t" --project=1',
                                    text=True,
                                    input=output_country,
                                    universal_newlines=True,
                                    shell=True
                                    )

    months = dates.split("\n")

    toaggregate = ""

    for month in months:
        if len(month) > 0:
            toaggregate = toaggregate + month[3:5] + "\n"

    minimum = subprocess.check_output('java Aggregate /min',
                                      text=True,
                                      input=toaggregate,
                                      universal_newlines=True,
                                      shell=True
                                      )
    minimum = minimum[0:-3]

    maximum = subprocess.check_output('java Aggregate /max',
                                      text=True, input=toaggregate, universal_newlines=True, shell=True)

    maximum = maximum[0:-3]

    deaths = {}

    for i in range(int(minimum), int(maximum) + 1):
        formated_month = ''
        if (i < 10):
            formated_month = f'0{i}'
        else:
            formated_month = str(i)
        output_month = subprocess.check_output(
            f'java process --delimiter="\t" --separator="\t" --select={formated_month}.2020',
            text=True,
            input=output_country,
            universal_newlines=True,
            shell=True)

        output_month_avg = subprocess.check_output(f'java process --delimiter="\t" --project=2 '
                                                   f'| java Aggregate /avg',
                                                   text=True,
                                                   input=output_month,
                                                   universal_newlines=True,
                                                   shell=True)

        output_month_avg = output_month_avg[0:-1]
        deaths[f'{i}.2020'] = float(output_month_avg)

    sorted_order = sorted(deaths.items(), key=lambda x: x[1], reverse=sortmode)
    result = ''

    for elem in sorted_order:
        result += str(elem[0]) + " " + str(elem[1]) + "\n"

    print(country)

    subprocess.run(f'java Head --lines={nLines}',
                   text=True,
                   input=result)
