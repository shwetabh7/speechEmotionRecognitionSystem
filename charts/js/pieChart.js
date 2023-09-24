import data from './jsonData.json' assert {type:'json'};
// console.log (data)

const ctx1 = document.getElementById('canvas_pie');

let speaker=[]
for(let i=0;i<data.length;i++){
    speaker.push(data[i].speaker)
}
// console.log(speaker)
const speaker_labels = speaker.filter((v, i, a) => a.indexOf(v) === i);

// console.log(speaker_labels)

function sumArray(array) {
    let sum = 0;
  
    array.forEach(item => {
      sum += item;
    });
  
    // console.log(sum);
    return sum;
  }

let percentage=[]
let a_duration=[]
let b_duration=[]
for(let i=0;i<data.length;i++){

    if(
        data[i].speaker===speaker_labels[0]
    ){
        let seg=data[i].end/1000-data[i].start/1000
        a_duration.push(seg)
    }
    else if(
        data[i].speaker===speaker_labels[1]
    )
    {
        let seg=data[i].end/1000-data[i].start/1000
        b_duration.push(seg)
    }
}

// console.log(a_duration)
// console.log(b_duration)

let tot_dur=sumArray(a_duration)+sumArray(b_duration)

let perc_A=sumArray(a_duration)*100/tot_dur
percentage.push(Math.round(perc_A))
let perc_B=sumArray(b_duration)*100/tot_dur
percentage.push(Math.round(perc_B))

// console.log(percentage)
  
  new Chart(ctx1,{
      type: 'pie',
      data:  {
        labels: speaker_labels,
        datasets: [{
          label: 'My First Dataset',
          data: percentage,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      }
    
    })