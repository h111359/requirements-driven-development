// Pokemon Battle Arena - Main Game Logic
// All code is vanilla JS, no external libraries

const canvas = document.getElementById('battle-canvas');
const ctx = canvas.getContext('2d');
const controls = document.getElementById('controls');
const infoPanel = document.getElementById('info-panel');

// Basic Pokemon data (can be expanded)
const POKEMON_LIST = [
    {
        name: 'Pikachu',
        hp: 100,
        attack: 30,
        defense: 15,
        sprite: 'pikachu',
        moves: ['Thunderbolt', 'Quick Attack', 'Iron Tail', 'Electro Ball']
    },
    {
        name: 'Charizard',
        hp: 120,
        attack: 35,
        defense: 20,
        sprite: 'charizard',
        moves: ['Flamethrower', 'Fly', 'Dragon Claw', 'Fire Spin']
    },
    {
        name: 'Bulbasaur',
        hp: 110,
        attack: 25,
        defense: 25,
        sprite: 'bulbasaur',
        moves: ['Vine Whip', 'Razor Leaf', 'Sleep Powder', 'Solar Beam']
    },
    {
        name: 'Squirtle',
        hp: 105,
        attack: 28,
        defense: 22,
        sprite: 'squirtle',
        moves: ['Water Gun', 'Bubble', 'Bite', 'Hydro Pump']
    }
];

let playerPokemon = null;
let enemyPokemon = null;
let playerHP = 0;
let enemyHP = 0;
let gameState = 'choose'; // choose, battle, end

// Animation state
let animFrame = 0;
let animTick = 0;
let animType = null; // 'idle', 'attack', 'hit', 'win', 'lose'
let animMove = null;
let animProgress = 0;

function drawPokemonSprite(pokemon, x, y, facing = 'right', frameIdx = 0, isAttacking = false, attackProgress = 0) {
    if (!pokemon) return;
    const sprite = window.SPRITES[pokemon.sprite];
    if (!sprite) return;
    const frame = sprite.frames[frameIdx % sprite.frames.length];
    ctx.save();
    ctx.translate(x + frame.dx, y + frame.dy);
    if (facing === 'left') ctx.scale(-1, 1);
    // Body
    ctx.beginPath();
    ctx.arc(0, 0, 60, 0, Math.PI * 2);
    ctx.fillStyle = sprite.color;
    ctx.fill();
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 4;
    ctx.stroke();
    // Eyes
    ctx.beginPath();
    ctx.arc(-20, -10, 8, 0, Math.PI * 2);
    ctx.arc(20, -10, 8, 0, Math.PI * 2);
    ctx.fillStyle = sprite.eye;
    ctx.fill();
    // Accent (cheeks, shell, etc.)
    ctx.beginPath();
    ctx.arc(-30, 20, 10, 0, Math.PI * 2);
    ctx.arc(30, 20, 10, 0, Math.PI * 2);
    ctx.fillStyle = sprite.accent;
    ctx.fill();
    // Tail (animated)
    ctx.save();
    ctx.rotate((frame.tailAngle + (isAttacking ? attackProgress * 30 : 0)) * Math.PI / 180);
    ctx.beginPath();
    ctx.moveTo(50, 0);
    ctx.lineTo(90, 10);
    ctx.lineWidth = 12;
    ctx.strokeStyle = sprite.tail;
    ctx.stroke();
    ctx.restore();
    // Name
    ctx.font = 'bold 20px Segoe UI';
    ctx.fillStyle = '#333';
    ctx.textAlign = 'center';
    ctx.fillText(pokemon.name, 0, 80);
    ctx.restore();
}

function drawBattle() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Animate attack/hit
    let playerFrame = animFrame;
    let enemyFrame = animFrame;
    let playerAttack = false;
    let enemyAttack = false;
    let playerAttackProgress = 0;
    let enemyAttackProgress = 0;
    if (animType === 'player-attack') {
        playerAttack = true;
        playerAttackProgress = animProgress;
    } else if (animType === 'enemy-attack') {
        enemyAttack = true;
        enemyAttackProgress = animProgress;
    }
    // Draw player Pokemon
    drawPokemonSprite(playerPokemon, 200, 250, 'right', playerFrame, playerAttack, playerAttackProgress);
    // Draw enemy Pokemon
    drawPokemonSprite(enemyPokemon, 600, 250, 'left', enemyFrame, enemyAttack, enemyAttackProgress);
    // Draw HP bars
    drawHPBar(playerHP, playerPokemon.hp, 120, 100, playerPokemon.name);
    drawHPBar(enemyHP, enemyPokemon.hp, 520, 100, enemyPokemon.name);
    // Draw attack effect
    if (animType === 'player-attack' && animProgress > 0.5) {
        drawAttackEffect('right');
    } else if (animType === 'enemy-attack' && animProgress > 0.5) {
        drawAttackEffect('left');
    }
}

function drawAttackEffect(side) {
    ctx.save();
    ctx.globalAlpha = 0.7;
    ctx.fillStyle = side === 'right' ? '#ffd700' : '#ff5252';
    let x = side === 'right' ? 400 : 400;
    let y = 250;
    ctx.beginPath();
    ctx.arc(x, y, 40 + Math.random() * 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
}

function drawHPBar(current, max, x, y, name) {
    ctx.save();
    ctx.fillStyle = '#fff';
    ctx.fillRect(x, y, 160, 24);
    ctx.strokeStyle = '#333';
    ctx.strokeRect(x, y, 160, 24);
    ctx.fillStyle = '#27ae60';
    let hpWidth = Math.max(0, 160 * (current / max));
    ctx.fillRect(x, y, hpWidth, 24);
    ctx.font = '16px Segoe UI';
    ctx.fillStyle = '#333';
    ctx.textAlign = 'left';
    ctx.fillText(`${name}: ${current} / ${max} HP`, x + 8, y + 18);
    ctx.restore();
}

function showInfo(msg) {
    infoPanel.textContent = msg;
}

function choosePokemon() {
    controls.innerHTML = '<h2>Choose Your Pokemon</h2>';
    POKEMON_LIST.forEach((poke, idx) => {
        const btn = document.createElement('button');
        btn.className = 'button';
        btn.textContent = poke.name;
        btn.onclick = () => startBattle(idx);
        controls.appendChild(btn);
    });
    showInfo('Select your Pokemon to begin the battle!');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    animType = 'idle';
    animFrame = 0;
}

function startBattle(playerIdx) {
    playerPokemon = POKEMON_LIST[playerIdx];
    playerHP = playerPokemon.hp;
    // Random enemy
    let enemyIdx;
    do {
        enemyIdx = Math.floor(Math.random() * POKEMON_LIST.length);
    } while (enemyIdx === playerIdx);
    enemyPokemon = POKEMON_LIST[enemyIdx];
    enemyHP = enemyPokemon.hp;
    gameState = 'battle';
    controls.innerHTML = '';
    playerPokemon.moves.forEach((move, idx) => {
        const btn = document.createElement('button');
        btn.className = 'button';
        btn.textContent = move;
        btn.onclick = () => playerAttack(idx);
        controls.appendChild(btn);
    });
    showInfo(`Battle Start! You (${playerPokemon.name}) vs Enemy (${enemyPokemon.name})`);
    animType = 'idle';
    animFrame = 0;
    drawBattle();
}

function playerAttack(moveIdx) {
    if (gameState !== 'battle') return;
    animType = 'player-attack';
    animMove = moveIdx;
    animProgress = 0;
    let moveName = playerPokemon.moves[moveIdx];
    let damage = playerPokemon.attack + Math.floor(Math.random() * 10) - enemyPokemon.defense;
    damage = Math.max(5, damage);
    setTimeout(() => {
        enemyHP -= damage;
        showInfo(`You used ${moveName}! Enemy ${enemyPokemon.name} took ${damage} damage.`);
        checkWin();
        setTimeout(enemyTurn, 1200);
    }, 700);
}

function enemyTurn() {
    if (gameState !== 'battle') return;
    animType = 'enemy-attack';
    animMove = Math.floor(Math.random() * enemyPokemon.moves.length);
    animProgress = 0;
    let moveName = enemyPokemon.moves[animMove];
    let damage = enemyPokemon.attack + Math.floor(Math.random() * 10) - playerPokemon.defense;
    damage = Math.max(5, damage);
    setTimeout(() => {
        playerHP -= damage;
        showInfo(`Enemy used ${moveName}! Your ${playerPokemon.name} took ${damage} damage.`);
        checkWin();
    }, 700);
}

function checkWin() {
    if (enemyHP <= 0) {
        gameState = 'end';
        enemyHP = 0;
        animType = 'win';
        drawBattle();
        showInfo(`Victory! You defeated ${enemyPokemon.name}!`);
        controls.innerHTML = '<button class="button" onclick="choosePokemon()">Play Again</button>';
    } else if (playerHP <= 0) {
        gameState = 'end';
        playerHP = 0;
        animType = 'lose';
        drawBattle();
        showInfo(`Defeat! Your ${playerPokemon.name} fainted!`);
        controls.innerHTML = '<button class="button" onclick="choosePokemon()">Play Again</button>';
    }
}

function animate() {
    animTick++;
    if (animTick % 10 === 0) {
        animFrame = (animFrame + 1) % 4;
    }
    if (animType === 'player-attack' || animType === 'enemy-attack') {
        animProgress += 0.08;
        if (animProgress > 1) {
            animType = 'idle';
            animProgress = 0;
        }
    }
    drawBattle();
    requestAnimationFrame(animate);
}

// Start game
choosePokemon();
animate();
