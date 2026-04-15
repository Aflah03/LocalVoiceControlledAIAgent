const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Enter triangle size: ', (size) => {
    const triangleSize = parseInt(size);
    for(let i=0;i<triangleSize;i++){
        let result = '';
        for(let j=0;j<triangleSize-i-1;j++)result += ' ';
        for(let k=0;k<=i;k++)result += '*';
        console.log(result);
    }
    rl.close();
});