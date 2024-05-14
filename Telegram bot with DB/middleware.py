import DB
def data_to_file(data,name,titles):
    r = open(f'{name}.csv','w+',encoding='utf-8')
    r.write(';'.join(titles)+'\n')
    for row in data:
      row=list(row)
      for i in range(len(row)):
        row[i]=str(row[i])
      r.write(';'.join(row)+'\n')
    r.close()
    f = open(f'{name}.csv',"rb")
    return f