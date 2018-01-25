import React, { Component } from 'react'

import Graph from '../Graph/Graph'

import style from './Home.scss'

const getTabNumber = () => {
  switch (window.location.pathname) {
    case '/actor':
      return -1
    case '/genre':
      return 0
    case '/keywords':
      return 1
    default:
      window.location.href = '/actor'
      return 0
  }
}

class Home extends Component {
  state = {
    currentTab: getTabNumber(),
    left: this.getLeft(getTabNumber()),
    tabs: ['Search By Actor', 'Search By Genre', 'Search By Keywords']
  }

  getLeft (tabNumber) {
    return `calc(50% + ${(tabNumber !== undefined ? tabNumber : this.state.currentTab) * 140}px)`
  }

  handleTabClicked (tabNumber) {
    window.location.href = (tabNumber === -1 && '/actor') || (tabNumber === 0 && '/genre') || '/keywords'
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
                  onClick={() => this.handleTabClicked(tabNumber)}
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
