#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>


void init(){
    fflush(stdin);
    setvbuf(stdout, 0, 2, 0);
    fflush(stderr);
    setvbuf(stderr, 0, 2, 0);
}

int attack = 0;

int money = 55;

void step1(){
    puts("You are a brave hero, and you have been teleported to a small town.");
    puts("You have arrived at the weapon store, and you are presented with three choices:");
    puts("1. Buy a dagger $5");
    puts("2. Purchase a large sword $50");
    puts("3. Purchase a Star Destroyer Cannon $500000000000000000");
    puts("4. Leave");

    int ch;

    while(ch != 4){
        
        printf("You have only $%d. Now your choice is:",money);
        scanf("%d",&ch);
        switch(ch){
            case 1: {
                if(money - 5 < 0) break;
                money -= 5;
                attack += 1;
                break;
            }
            case 2: {
                if(money - 50 < 0) break;
                money -= 50;
                attack += 20;
                break;
            }
            case 3: {
                puts("You must be dreaming, buddy!");
                break;
            }
            case 4: {
                break;
            }
            default: {
                puts("No this choice!");
                break;
            }
        }
    }

    printf("Your current attack power is %d. Now let us go!\n",attack);

    return ;
}

int boss = 1000;
int hp = 50;

void step2(){
    puts("You have arrived at the dragon's lair. Let the battle commence!");
    int ch;
    while(boss > 0 && hp > 0){
        printf("Boss->%d, You->%d\n",boss,hp);
        puts("1. Attack!");
        puts("2. Escape!");
        puts(">>");
        scanf("%d",&ch);
        switch(ch){
            case 1:{
                boss -= attack;
                if(boss <= 0) break;
                hp -= 1;
                break;
            }
            case 2:{
                puts("Bye bye!");
                exit(0);
                break;
            }
            default:{
                puts("No this choice!");
                break;
            }
        }
        if(boss <= 0) break;
    }
    if(hp <= 0) {
        puts("Defeat!");
        exit(0);
    }
    puts("You defeated the dragon!");
    return;
}

void step3(){
    printf("You have arrived at the small tavern opened by Longque, and you still have $%d\n",money);
    int ch;
    while(1){
        puts("You have three choices:");
        puts("1. buy beer");
        puts("2. buy the tavern");
        puts("3. leave");
        puts("Your choice:");
        scanf("%d",&ch);
        switch(ch){
            case 1:{
                if(money <= 0){
                    puts("aha?");
                    exit(0);
                }
                puts("beer: $3/bundle");
                puts("how many?");
                int x;
                scanf("%d",&x);
                if(x < 0){
                    puts("aha?");
                    break;
                }
                money -= x * 3;
                printf("You still have $%d\n",money);
                break;
            }
            case 2:{
                puts("Longque offers $2,000,000");
                printf("You still have $%d\n",money);
                if(money < 2000000){
                    puts("You do not have enough money!");
                    break;
                }
                else{
                    puts("You got it!");
                    system("/bin/sh");
                    exit(0);
                    break;
                }
                break;
            }
            case 3:{
                exit(0);
                break;
            }
            default:{
                puts("No this choice!");
                break;
            }

        }
    }


}



int main(){
    init();
    step1();
    step2();
    step3();
    return 0;
}

//gcc -o game game.c