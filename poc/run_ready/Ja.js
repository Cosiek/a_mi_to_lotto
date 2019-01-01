
function lotto(money, bet_cost, history){
    bets = [];
    while (money >= bet_cost){
        bets.push([randInt(), randInt(), randInt(), randInt(), randInt(), randInt()]);
        money -= bet_cost;
    }
    return bets
}

function randInt(){
    return Math.floor(Math.random() * (49 - 1)) + 1;
}

console.log(lotto(100, 7, []))
