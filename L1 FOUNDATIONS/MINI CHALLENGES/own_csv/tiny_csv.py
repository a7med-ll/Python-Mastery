def parse_csv(filepath):

    rows =[]

    with open(filepath,'r') as f:

        for line in f:
            line = line.strip()

            if line:
                values = line.split(',')
                rows.append(values)

    return rows

rows = parse_csv("test.csv")
for row in rows:
    print(row)