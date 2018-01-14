import React, { Component } from 'react'

import Graph from '../Graph/Graph'

import style from './Home.scss'

class Home extends Component {
  state = {
    currentTab: -1,
    left: this.getLeft(-1),
    tabs: ['Search By Actor', 'Search By Genre', 'Search By Year']
  }

  getLeft (tabNumber) {
    return `calc(50% + ${(tabNumber !== undefined ? tabNumber : this.state.currentTab) * 120}px)`
  }

  render () {
    const { currentTab, tabs, left } = this.state
    return (
      <div>
        <div
          className={style.buttonRow}
          onMouseOut={() => this.setState({ left: this.getLeft() })}
        >
          {
            tabs.map((tab, i, arr) => {
              const tabNumber = i - Math.floor(arr.length / 2)
              return (
                <button
                  key={tabNumber}
                  onMouseOver={() => this.setState({ left: this.getLeft(tabNumber) })}
                  onClick={() => this.setState({ currentTab: tabNumber })}
                  style={{ color: tabNumber === currentTab ? '#0091ff' : 'black' }}
                >
                  {tab}
                </button>
              )
            })
          }
        </div>
        <div className={style.bottomLine} style={{ left }} />
        <Graph currentTab={currentTab} />
      </div>
    )
  }
}

export default Home
