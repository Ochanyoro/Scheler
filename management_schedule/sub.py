
def output_excel(request):
    ex = Document.objects.filter(description="manten").first()
    #print(ex.document.url)
    wb = xlrd.open_workbook('.'+str(ex.document.url))
    sheet = wb.sheet_by_name('Sheet1')
    l_2d_all = get_list_2d_all(sheet)
    l_2d_all = np.array(l_2d_all).T
    name_list =[]
    #名前のみを抽出する
    for i in range(2,len(l_2d_all[0])):
        if l_2d_all[0][i] != "":
            name_list.append(l_2d_all[0][i])
    print(name_list)
    weekname = ["火","水","木","金","土","日"]
    weekkoma =[3,3,3,3,6,6]

    kari = []
    l_2d_all = l_2d_all.T
    print(l_2d_all.shape)
    schedule={}
    for i in range(0,len(name_list)):
        a=0
        people ={}
        for week in range(0,len(weekname)):
            now =[]
            for j in range(0,weekkoma[week]):
                a=a+1
                people_kari =[]
                student = []
                content = []
                if l_2d_all[i*4+2][a] != "":
                    #print(l_2d_all[i*4+1][a])
                    student.append(l_2d_all[i*4+2][a])
                    content.append(l_2d_all[i*4+3][a])
                if l_2d_all[i*4+4][a] != "":
                    #print(l_2d_all[i*4+3][a])
                    student.append(l_2d_all[i*4+4][a])
                    content.append(l_2d_all[i*4+5][a])
                if student != []:
                    people_kari.append(student)
                    people_kari.append(content)
                now.append(people_kari)
                #print(now)
            people[weekname[week]] = now
        schedule[name_list[i]] = people
    print(schedule["大和田"])

    x =excel_date(int(float(l_2d_all[0][0])))
    print(x)

    normal =datetime.datetime(2021, 1, 1, 12, 45, 0)
    zikan =["A","B","C","D","E","F"]
    gp = Group.objects.filter(title="number1のk").first()
    for name in name_list:
        people = schedule[name]
        now_user = CustomUser.objects.filter(last_name=name).first()
        j=0
        for week in weekname:
            day_schedule = people[week]
            i=0
            k=3
            for koma in day_schedule:
                if week == "土" or week == "日":
                    if koma!=[]:
                        sc =Schedule()
                        sc.owner = now_user
                        sc.group = gp
                        sc.Nickname = name
                        sc.summary = zikan[i]
                        if len(koma[0]) == 2:
                            sc.description = koma[0][0]+":"+koma[1][0]+koma[0][1]+":"+koma[1][1]
                        else:
                            sc.description = koma[0][0]+":"+koma[1][0]
                        sc.start_time = (normal + timedelta(seconds=5400*(1+i))).time()
                        sc.end_time   = (normal + timedelta(seconds=5400*(2+i)) - timedelta(minutes=10)).time()
                        sc.date = x + timedelta(days = 1*j)
                        sc.save()
                    i=i+1
                else :
                    if koma!=[]:
                        sc =Schedule()
                        sc.owner = now_user
                        sc.group = gp
                        sc.Nickname = name
                        sc.summary = zikan[k]
                        if len(koma[0]) == 2:
                            sc.description = koma[0][0]+":"+koma[1][0]+koma[0][1]+":"+koma[1][1]
                        else:
                            sc.description = koma[0][0]+":"+koma[1][0]
                        sc.start_time = (normal + timedelta(seconds=5400*(1+k))).time()
                        sc.end_time   = (normal + timedelta(seconds=5400*(2+k)) - timedelta(minutes=10)).time()
                        sc.date = x + timedelta(days = 1*j)
                        sc.save()
                    k=k+1
            j=j+1

    params = {
        'ex':ex,
    }
    return render(request,'schedule/output_excel.html',params)
