import data from './jsonData.json' assert {type:'json'};
console.log(data[8].dbfs);
    
const ctx = document.getElementById('canvas')  

let speaker=[]
for(let i=0;i<data.length;i++){
    speaker.push(data[i].speaker)
}
// console.log(speaker)
const speaker_labels = speaker.filter((v, i, a) => a.indexOf(v) === i);

let speakerStart=[]
let speakerEnd=[]
for(let i=0;i<data.length;i++){
  if(speaker[i]===speaker_labels[0]){
    speakerStart.push(Math.round(data[i].start))
    speakerEnd.push(Math.round(data[i].end))
  }  
}
console.log(speakerStart)
console.log(speakerEnd)

let labelX=(Math.ceil((data[data.length-1].end)/1000)+5)
let label_X=[0]
let sum=0
for(let i=0;i<labelX;i++){
  sum=sum+0.5
  label_X.push(sum)
}

console.log(speaker)

console.log(label_X)

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: [12.154,12.154,12.354,12.454,12.554,12.654,12.754,12.854,12.954,13.054,13.154,13.354,13.454,13.502],
      datasets: [{
        label: 'speaker A',
        data: [
          { x: 12.154, y: 0 },
          { x: 12.154, y: -43.989591790056004},
          { x: 12.354, y: -18.403484463152367 },
          { x: 12.454, y: -31.75133049258022 },
          { x: 12.554, y: -20.894910104738592 },
          { x: 12.654, y: -21.70104687145502 },
          { x: 12.754, y: -20.084704676466597},
          { x: 12.854, y: -25.985680653474496 },
          { x: 12.954, y: -41.71395309914619 },
          { x: 13.054, y: -24.830463097183845 },
          { x: 13.154, y: -20.01273279920865 },
          { x: 13.254, y: -20.56057447200487},
          { x: 13.354, y: -22.43398589223275 },
          { x: 13.554, y: -42.77745955806411 },
          { x: 13.502, y: -39.52747672333882 }
          ],
        background:'white',
        borderColor:'red',
        borderWidth: 2,
        
      },
      {
        label: 'speaker B',
        data: [-20.6,-35.7,-33.46,-28.27,-44.89,-11.19, -36.78],
        background:'white',
        borderColor:'rgb(54, 162, 235)',
        borderWidth: 2,
        
      }  
    ]
    },
    options: {
        elements:{
            line:{
                tension:0
            }
        },
        scales: {
        x:{
            display: true,
            title:{
                display:true,
                text:'dBFS Levels'
            }
        },    
            
        y: {
            display:true,
            beginAtZero: true,
              title:{
                  display:true,
                  text:'Time in seconds'
              }
          }
      }
    }
  });


