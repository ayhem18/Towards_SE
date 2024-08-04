// setup canvas

const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const width = (canvas.width = window.innerWidth);
const height = (canvas.height = window.innerHeight);

// function to generate random number

function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// function to generate random color

function randomRGB() {
  return `rgb(${random(0, 255)},${random(0, 255)},${random(0, 255)})`;
}

// create the Ball class

class BallParent {
    constructor(x, y, velX, velY, color, size) {
        this.x = x;
        this.y = y;
        this.velX = velX;
        this.velY = velY;
        this.color = color;
        this.size = size;
    }

    update() {
        // if the ball crosses the canvas right wall
        if ((this.x + this.size) >= width) {
            this.velX = -(this.velX);
        }
    
        // if the ball crosses the canvas left wall
        if ((this.x - this.size) <= 0) {
            this.velX = -(this.velX);
        }
    
        if ((this.y + this.size) >= height) {
            this.velY = -(this.velY);
        }
    
        if ((this.y - this.size) <= 0) {
            this.velY = -(this.velY);
        }
    
        this.x += this.velX;
        this.y += this.velY;
    }

    collide(anotherBall) {
    }
}

class EvilBall extends BallParent{
    constructor(x, y, valX, valY) {
        super(x, y, valX, valY, size=10, color="white");
    }
}


class Ball extends BallParent {
    constructor(x, y, valX, valY) {
        super(x, y, valX, valY, size=random(2, 6), color=randomRGB());
    }
}

function draw(ball) {
    ctx.beginPath();
    ctx.fillStyle = ball.color;
    ctx.arc(ball.x, ball.y, ball.size, 0, 2 * Math.PI);
    ctx.fill();
}


function detectCollision(balls) {
    // the first step is to sort the balls by their 'x' coordinate
    balls.sort((b1, b2) => b1.x - b2.x);

    let n = balls.length;
    let intersect_on_x = [];
    let current_set = [balls[0]];
    
    let start = 0; let end = 1;

    while (end < n) {
        while (end < n && balls[start].x + balls[start].size > balls[end].x - balls[end].size) {
            end += 1;
            current_set.push(balls[end]);
        }

        intersect_on_x.push(current_set)

        if (end == n) {
            break;
        }

        while (balls[start].x + balls[start].size <= balls[end].x - balls[end].size) {
            // remove the first element
            current_set = current_set.slice(1);
            start ++;
        }
        
        // add the ball at the end position
        current_set.push(ball[end]);
        end ++;
    }

    



}

// class Ball

// class Ball {


//     collisionDetect() {
//         for (const ball of balls) {
//             if (this !== ball) {
//                 const dx = this.x - ball.x;
//                 const dy = this.y - ball.y;
//                 const distance = Math.sqrt(dx * dx + dy * dy);

//                 if (distance < this.size + ball.size) {
//                     ball.color = this.color = randomRGB();
//                 }
//             }
//         }
//     }
// }

// const balls = [];

// while (balls.length < 10) {
//   const size = random(10, 20);
//   const ball = new Ball(
//     // ball position always drawn at least one ball width
//     // away from the edge of the canvas, to avoid drawing errors
//     random(0 + size, width - size),
//     random(0 + size, height - size),
//     random(-7, 7),
//     random(-7, 7),
//     randomRGB(),
//     size,
//   );

//   balls.push(ball);
// }


// function loop() {
//     ctx.fillStyle = "rgb(0 0 0 / 25%)";
//     ctx.fillRect(0, 0, width, height);
  
//     for (const ball of balls) {
//       ball.draw();
//       ball.update();
//       ball.collisionDetect();
//     }
  
//     requestAnimationFrame(loop);
// }

// loop();
