import subprocess
import sys

if __name__ == '__main__':
    continent = ''
    month = ''
    year = ''
    for param in sys.argv:
        if param.find("--continent=") != -1:
            continent = param.replace("--continent=", "")
        elif param.find("--month=") != -1:
            month = param.replace("--month=", "")
        elif param.find("--year=") != -1:
            year = param.replace("--year=", "")

    date = f'{month}.{year}'
    print(continent + '   ' + date)
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

    output_month = ''
    try:
        output_month = subprocess.check_output(
            f'java process --delimiter="\t" --project=1,5,11'
            f'| java process --select={date}',
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

    subprocess.run(f'java process --delimiter="\t\t" --project=2 '
                   f'| java Aggregate /sum',
                   shell=True,
                   universal_newlines=True,
                   input=output_month)
