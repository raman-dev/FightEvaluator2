<script setup>

import { useMatchupStore } from '@/stores/matchupStore';
import { useMatchupActionMenuStore } from '@/stores/matchupActionMenuStore';
import {defineModel, onMounted, useTemplateRef,watch} from 'vue';
import { storeToRefs } from 'pinia';

const matchupActionMenuStore = useMatchupActionMenuStore();
const { menuOpen,menuPosition,menuLimitRect } = storeToRefs(matchupActionMenuStore);
const menuRef = useTemplateRef('menu');

const { activeMatchup } = storeToRefs(useMatchupStore());

function position () {
    const matchup = activeMatchup.value.matchup;
    const menu = menuRef.value;

    console.log(menuPosition.value);
    
    let watchIcon = menu.querySelector('#watch-icon');
    let unwatchIcon = menu.querySelector('#unwatch-icon');
    let watchMenuLabel = menu.querySelector('.watch-menu-item span');

    if (matchup.inWatchList === true){
        watchIcon.classList.add('d-none');//hide watch icon
        unwatchIcon.classList.remove('d-none');
        watchMenuLabel.textContent = 'unwatch';
    }
    else{
        watchIcon.classList.remove('d-none');//show watch icon
        unwatchIcon.classList.add('d-none');
        watchMenuLabel.textContent = 'watch';
    }
    
    //how to check if menu is offscreen?
    //x + width < pageX + containerWidth -> within page
    //y + height < pageY + containerHeight -> within page
    
    //menu.x + width cannot go beyond limitrect right
    const limitRect = menuLimitRect.value;
    const right = limitRect.left + limitRect.width + window.scrollX;
    const bottom = limitRect.top + limitRect.height + window.scrollY;
    
    let left = menuPosition.value.x;//
    let top = menuPosition.value.y;
    
    if (left + menu.clientWidth > right){
        left -= (left + menu.clientWidth) - right;
    }
    if (top + menu.clientHeight > bottom){
        top -= (top + menu.clientHeight) - bottom;
    }
    
    menu.style.left = `${left}px`;
    menu.style.top = `${top}px`;

};

function onEnter(menuContainer){
    position();
}


</script>
<template>
    <Transition  @enter="onEnter">
    <div class="matchup-actions-menu-container " ref="menu" v-if="menuOpen">
        <ul class="menu-item-list" >
            <li class="menu-list-item">
                <div class="menu-item watch-menu-item" >
                    <svg id="unwatch-icon" class="d-none" xmlns="http://www.w3.org/2000/svg" height="24px"
                        viewBox="0 -960 960 960" width="24px" fill="#5f6368">
                        <path
                            d="m644-428-58-58q9-47-27-88t-93-32l-58-58q17-8 34.5-12t37.5-4q75 0 127.5 52.5T660-500q0 20-4 37.5T644-428Zm128 126-58-56q38-29 67.5-63.5T832-500q-50-101-143.5-160.5T480-720q-29 0-57 4t-55 12l-62-62q41-17 84-25.5t90-8.5q151 0 269 83.5T920-500q-23 59-60.5 109.5T772-302Zm20 246L624-222q-35 11-70.5 16.5T480-200q-151 0-269-83.5T40-500q21-53 53-98.5t73-81.5L56-792l56-56 736 736-56 56ZM222-624q-29 26-53 57t-41 67q50 101 143.5 160.5T480-280q20 0 39-2.5t39-5.5l-36-38q-11 3-21 4.5t-21 1.5q-75 0-127.5-52.5T300-500q0-11 1.5-21t4.5-21l-84-82Zm319 93Zm-151 75Z" />
                    </svg>
                    <svg id="watch-icon" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960"
                        width="24px" fill="#5f6368">
                        <path
                            d="M480-320q75 0 127.5-52.5T660-500q0-75-52.5-127.5T480-680q-75 0-127.5 52.5T300-500q0 75 52.5 127.5T480-320Zm0-72q-45 0-76.5-31.5T372-500q0-45 31.5-76.5T480-608q45 0 76.5 31.5T588-500q0 45-31.5 76.5T480-392Zm0 192q-146 0-266-81.5T40-500q54-137 174-218.5T480-800q146 0 266 81.5T920-500q-54 137-174 218.5T480-200Zm0-300Zm0 220q113 0 207.5-59.5T832-500q-50-101-144.5-160.5T480-720q-113 0-207.5 59.5T128-500q50 101 144.5 160.5T480-280Z" />
                    </svg>
                    <span>&nbsp;watch</span>
                </div>
            </li>
            <li class="menu-list-item">
                <div class="menu-item" >
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                        fill="#5f6368">
                        <path
                            d="M280-280h80v-200h-80v200Zm320 0h80v-400h-80v400Zm-160 0h80v-120h-80v120Zm0-200h80v-80h-80v80ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z" />
                    </svg>
                    <span>&nbsp;analyze</span>
                </div>
            </li>

            <li class="menu-list-item">
                <div class="menu-item" >
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                        fill="#5f6368">
                        <path
                            d="M160-400v-80h280v80H160Zm0-160v-80h440v80H160Zm0-160v-80h440v80H160Zm360 560v-123l221-220q9-9 20-13t22-4q12 0 23 4.5t20 13.5l37 37q8 9 12.5 20t4.5 22q0 11-4 22.5T863-380L643-160H520Zm300-263-37-37 37 37ZM580-220h38l121-122-18-19-19-18-122 121v38Zm141-141-19-18 37 37-18-19Z" />
                    </svg>
                    <span>edit</span>
                </div>
            </li>
            <li class="menu-list-item">
                <div class="menu-item delete-menu-item" >
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                        fill="#CC3323">
                        <path
                            d="m376-300 104-104 104 104 56-56-104-104 104-104-56-56-104 104-104-104-56 56 104 104-104 104 56 56Zm-96 180q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520Zm-400 0v520-520Z" />
                    </svg>
                    <span>delete</span>
                </div>
            </li>
        </ul>
    </div>
    </Transition>
    
</template>
<style lang="scss" scoped>
.matchup-actions-menu-container {
    position: absolute;
    top: 0%;
    left: 0%;
    z-index: 1000;
    min-width: 13.5ch;

    ul.menu-item-list {
        margin: 0px;
        padding: 0px;
        background-color: #111519;
        box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px;

        border: 1px solid gray;
        border-radius: 0.6rem;
        overflow: hidden;


        li.menu-list-item {
            list-style: none;
            border-top: 1px solid gray;
        }

        li.menu-list-item:first-child {
            border-top: none;
        }

    }

    li.menu-list-item:hover {
        cursor: pointer;
        background-color: violet;
        color: black;
    }

    .menu-item {
        text-transform: capitalize;
        padding: 0.6rem;
    }
}
</style>