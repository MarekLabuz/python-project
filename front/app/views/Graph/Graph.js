import React, { Component } from 'react'
import * as d3 from 'd3'
import cx from 'classnames'

import SearchBar from '../../components/SearchBar/SearchBar'

import style from './Graph.scss'

// const data = {
//   nodes: [
//     { id: 'Mother', group: 'film' },
//     { id: 'Pasażerowie', group: 'film' },
//     { id: 'Bałwanek', group: 'film' },
//     { id: 'X-Men', group: 'film' },
//     { id: 'Fassbender', group: 'actor' },
//     { id: 'Lawrence', group: 'actor' },
//     { id: 'Kilmer', group: 'actor' }
//   ],
//   links: [
//     { source: 'Bałwanek', target: 'Fassbender', value: 1 },
//     { source: 'Bałwanek', target: 'Kilmer', value: 1 },
//     { source: 'X-Men', target: 'Fassbender', value: 1 },
//     { source: 'X-Men', target: 'Lawrence', value: 1 },
//     { source: 'Pasażerowie', target: 'Lawrence', value: 1 },
//     { source: 'Mother', target: 'Lawrence', value: 1 }
//   ]
// }

const data = {
  nodes: [
    { id: 0, title: 'Click Me!', group: 'film' }
  ],
  links: []
}

class Graph extends Component {
  constructor () {
    super()

    this.ticked = this.ticked.bind(this)
    this.dragstarted = this.dragstarted.bind(this)
    this.dragged = this.dragged.bind(this)
    this.dragended = this.dragended.bind(this)
    this.handleNodeClick = this.handleNodeClick.bind(this)

    this.state = {
      emptyGraph: true,
      searchVisible: false,
      searchOpen: true
    }
  }

  componentDidMount () {
    const svg = d3.select('svg')
    const width = svg.attr('width')
    const height = svg.attr('height')

    const color = d3.scaleOrdinal(d3.schemeCategory20)

    this.simulation = d3.forceSimulation()
      .force('link', d3.forceLink().distance(100).id(d => d.id))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width / 2, height / 2))

    // d3.json('miserables.json', function (error, graph) {
    //   if (error) throw error

    this.link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(data.links)
      .enter()
      .append('line')
      .attr('stroke-width', d => Math.sqrt(d.value))

    this.node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(data.nodes)
      .enter()
      .append('circle')
      .attr('r', 9)
      .attr('fill', d => color(d.group))
      .call(d3.drag()
        .on('start', this.dragstarted)
        .on('drag', this.dragged)
        .on('end', this.dragended))

    this.textLabels = svg.append('g')
      .attr('class', 'textLabels')
      .selectAll('text')
      .data(data.nodes)
      .enter()
      .append('text')
      .text(d => d.title)
      .attr('font-family', 'sans-serif')
      .attr('font-size', '14px')
      .attr('fill', 'black')

    this.node.on('click', this.handleNodeClick)

    this.node.append('title')
      .text(d => d.id)

    this.simulation
      .nodes(data.nodes)
      .on('tick', this.ticked)

    this.simulation.force('link')
      .links(data.links)
    // }
    this.showSearchPopup()
  }

  ticked () {
    this.link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    this.node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)

    this.textLabels
      .attr('dx', function dx (d) {
        return d.x - (this.getComputedTextLength() / 2)
      })
      .attr('dy', d => d.y - 15)
  }

  dragstarted (d) {
    if (!d3.event.active) this.simulation.alphaTarget(0.3).restart()
    d.fx = d.x
    d.fy = d.y
  }

  dragged (d) {
    d.fx = d3.event.x
    d.fy = d3.event.y
  }

  dragended (d) {
    if (!d3.event.active) this.simulation.alphaTarget(0)
    d.fx = null
    d.fy = null
  }

  showSearchPopup () {
    this.setState({
      searchVisible: true,
      searchOpen: false
    }, () => {
      setTimeout(() => {
        this.setState({
          searchOpen: true
        })
      }, 25)
    })
  }

  hideSearchPopup () {
    this.setState({
      searchOpen: false
    }, () => {
      setTimeout(() => {
        this.setState({
          searchVisible: false
        })
      }, 400)
    })
  }

  handleNodeClick () {
    const { emptyGraph } = this.state
    if (emptyGraph) {
      this.showSearchPopup()
    }
  }

  render () {
    const { searchVisible, searchOpen } = this.state
    return [
      <svg key="svg" width={window.innerWidth} height={window.innerHeight} />,
      searchVisible && (
        <div
          key="search"
          className={cx(style.searchBackground, searchOpen && style.searchBackgroundOpen)}
        >
          <div className={cx(style.search, searchOpen && style.searchOpen)}>
            <SearchBar />
          </div>
        </div>
      )
    ]
  }
}

export default Graph
