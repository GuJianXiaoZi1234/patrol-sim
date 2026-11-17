<script setup>
import { reactive } from 'vue'

const cellSize = 36

const map = {
  width: 16,
  height: 12,
}

const robot = reactive({
  x: 1,
  y: 1,
  heading: 90,
  status: 'idle',
})

// 暂定模拟规则：0 向上、90 向右、180 向下、270 向左
function move(step) {
  let nextX = robot.x
  let nextY = robot.y

  if (robot.heading === 0) {
    nextY = nextY - step
  } else if (robot.heading === 90) {
    nextX = nextX + step
  } else if (robot.heading === 180) {
    nextY = nextY + step
  } else if (robot.heading === 270) {
    nextX = nextX - step
  }

  if (
    nextX >= 0 &&
    nextX < map.width &&
    nextY >= 0 &&
    nextY < map.height
  ) {
    robot.x = nextX
    robot.y = nextY
    robot.status = 'idle'
  } else {
    robot.status = 'blocked'
  }
}

function moveForward() {
  move(1)
}

function moveBack() {
  move(-1)
}

function turnLeft() {
  robot.heading = (robot.heading + 270) % 360
  robot.status = 'idle'
}

function turnRight() {
  robot.heading = (robot.heading + 90) % 360
  robot.status = 'idle'
}
</script>

<template>
  <main>
    <h1>智能巡检机器人</h1>
    <p>模拟数据模式 · 地图预览</p>

    <svg
      :viewBox="`0 0 ${map.width * cellSize} ${map.height * cellSize}`"
      aria-label="巡检地图"
      role="img"
      style="display: block; width: 100%; max-width: 576px; background: white; border: 2px solid #334155;"
    >
      <!-- 竖线：16 列需要 17 条边线 -->
      <line
        v-for="n in map.width + 1"
        :key="`column-${n}`"
        :x1="(n - 1) * cellSize"
        y1="0"
        :x2="(n - 1) * cellSize"
        :y2="map.height * cellSize"
        stroke="#cbd5e1"
      />

      <!-- 横线：12 行需要 13 条边线 -->
      <line
        v-for="n in map.height + 1"
        :key="`row-${n}`"
        x1="0"
        :y1="(n - 1) * cellSize"
        :x2="map.width * cellSize"
        :y2="(n - 1) * cellSize"
        stroke="#cbd5e1"
      />

      <!-- 机器人：放在对应格子内，四周留一点空隙 -->
      <rect
        :x="robot.x * cellSize + 4"
        :y="robot.y * cellSize + 4"
        :width="cellSize - 8"
        :height="cellSize - 8"
        rx="6"
        fill="#f97316"
      />
      <text
  :x="(robot.x + 0.5) * cellSize"
  :y="(robot.y + 0.5) * cellSize"
  text-anchor="middle"
  dominant-baseline="central"
  font-size="20"
  fill="white"
>
  {{ { 0: '↑', 90: '→', 180: '↓', 270: '←' }[robot.heading] }}
</text>
    </svg>
    <button @click="turnLeft">左转</button>
    <button @click="moveForward">前进</button>
    <button @click="moveBack">后退</button>
    <button @click="turnRight">右转</button>
    <p>
      位置：({{ robot.x }}, {{ robot.y }})
      · 朝向：{{ robot.heading }}°
      · 状态：{{ robot.status }}
    </p>
  </main>
</template>
