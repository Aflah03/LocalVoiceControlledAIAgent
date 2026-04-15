const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Enter triangle size: ', size => {
    const height = parseInt(size) + 1;
    for (let i = 0; i < height; i++) {
        let numSpaces = ' '.repeat(height - i - 1);
        let numAsterisks = '*'.repeat(i + 1);

        process.stdout.write(numSpaces + numAsterisks + '\n');
    }

    rl.close();
});