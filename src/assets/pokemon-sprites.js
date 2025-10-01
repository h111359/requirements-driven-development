// Simple animated sprite data for Pokemon
// Each sprite is a set of colored shapes and animation frames
// No external images used, all drawn with canvas

const SPRITES = {
    pikachu: {
        color: '#ffe066',
        accent: '#f7b32b',
        eye: '#333',
        tail: '#f7b32b',
        frames: [
            { dx: 0, dy: 0, tailAngle: 0 },
            { dx: 4, dy: -2, tailAngle: 10 },
            { dx: -4, dy: 2, tailAngle: -10 },
            { dx: 0, dy: 0, tailAngle: 0 }
        ]
    },
    charizard: {
        color: '#ff7043',
        accent: '#ffb300',
        eye: '#222',
        tail: '#ffb300',
        frames: [
            { dx: 0, dy: 0, tailAngle: 0 },
            { dx: 6, dy: -3, tailAngle: 15 },
            { dx: -6, dy: 3, tailAngle: -15 },
            { dx: 0, dy: 0, tailAngle: 0 }
        ]
    },
    bulbasaur: {
        color: '#7ed957',
        accent: '#4caf50',
        eye: '#222',
        tail: '#4caf50',
        frames: [
            { dx: 0, dy: 0, tailAngle: 0 },
            { dx: 3, dy: -2, tailAngle: 8 },
            { dx: -3, dy: 2, tailAngle: -8 },
            { dx: 0, dy: 0, tailAngle: 0 }
        ]
    },
    squirtle: {
        color: '#4fc3f7',
        accent: '#fff176',
        eye: '#222',
        tail: '#fff176',
        frames: [
            { dx: 0, dy: 0, tailAngle: 0 },
            { dx: 2, dy: -2, tailAngle: 5 },
            { dx: -2, dy: 2, tailAngle: -5 },
            { dx: 0, dy: 0, tailAngle: 0 }
        ]
    }
};

window.SPRITES = SPRITES;
