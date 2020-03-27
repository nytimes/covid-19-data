console.log('nytcovid19.js loaded');

nytcovid19={
    date:Date(),
    data:{}, // cache it here
    urlStates:'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv',
    urlCounties:'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
}



nytcovid19.getData=async(urlStates=nytcovid19.urlStates,urlCounties=nytcovid19.urlCounties)=>{
    let txt = await (await fetch(urlStates)).text()
    let arr =txt.split(/[\n\r]+/).map(r=>r.split(','))
    let labels=arr[0]
    let dt={}
    arr.slice(1).forEach(r=>{
        dt[r[1]]={}
        dt[r[1]][labels[0]]=new Date(r[0])   // date
        dt[r[1]][labels[2]]=parseFloat(r[2]) // fips
        dt[r[1]][labels[3]]=parseFloat(r[3]) // cases
        dt[r[1]][labels[4]]=parseFloat(r[4]) // deaths
    })
    txt = await (await fetch(urlCounties)).text()
    arr =txt.split(/[\n\r]+/).map(r=>r.split(','))
    labels=arr[0]
    arr.slice(1).forEach(r=>{
        if(!dt[r[2]].counties){
            dt[r[2]].counties={}
        }
        dt[r[2]].counties[r[1]]={}
        dt[r[2]].counties[r[1]][labels[0]]=new Date(r[0]) //date
        dt[r[2]].counties[r[1]][labels[3]]=parseFloat(r[3]) // fips
        dt[r[2]].counties[r[1]][labels[4]]=parseFloat(r[4]) // cases
        dt[r[2]].counties[r[1]][labels[5]]=parseFloat(r[5]) // deaths
    })
    return dt
}



if(typeof(define)!='undefined'){
    define(nytcovid19)
}