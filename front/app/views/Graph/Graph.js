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

// const data = {
//   nodes: [
//     { id: 0, title: 'Click Me!', group: 'film' }
//   ],
//   links: []
// }

class Graph extends Component {
  constructor () {
    super()

    this.ticked = this.ticked.bind(this)
    this.dragstarted = this.dragstarted.bind(this)
    this.dragged = this.dragged.bind(this)
    this.dragended = this.dragended.bind(this)
    this.handleNodeClick = this.handleNodeClick.bind(this)
    this.hideSearchPopup = this.hideSearchPopup.bind(this)
    this.handleDataUpdate = this.handleDataUpdate.bind(this)

    this.state = {
      searchVisible: false,
      searchOpen: true,
      data: {
        nodes: [
          { id: 0, title: 'Click Me!', group: 'mock' }
        ],
        links: []
      }
    }

    this.radius = 15
  }

  componentDidMount () {
    this.renderGraph()
  }

  componentDidUpdate (prevProps, prevState) {
    if (prevState.data !== this.state.data) {
      this.updateGraph()
    }
  }

  handleNodeClick (node) {
    if (node.group === 'mock' || node.group === 'person') {
      const { x, y } = node
      this.popupX = x
      this.popupY = y
      this.showSearchPopup(node)
    }
  }

  hideSearchPopup () {
    this.setState({
      searchOpen: false
    }, () => {
      setTimeout(() => {
        this.setState({
          searchVisible: false
        })
      }, 200)
    })
  }

  showSearchPopup (node) {
    this.setState({
      searchVisible: true,
      searchOpen: false,
      node
    }, () => {
      setTimeout(() => {
        this.setState({
          searchOpen: true
        })
      }, 25)
    })
  }

  handleDataUpdate (film) {
    const nodesIds = [film.id, ...film.people.map(person => person.id)]
    const linksIds = film.people.map(person => ({ source: film.id, target: person.id }))
    this.setState(state => ({
      data: {
        nodes: state.data.nodes
          .filter(({ id }) => !nodesIds.includes(id) && id !== 0)
          .concat([{ id: film.id, title: film.title, group: 'film' }])
          .concat(film.people.map(person => ({ id: person.id, title: person.name, group: 'person' }))),
        links: state.data.links
          .filter(({ source, target }) => !linksIds.some(link => link.source === source.id && link.target === target.id))
          .map(link => ({ ...link, source: link.source.id, target: link.target.id }))
          .concat(film.people.map(person => ({
            source: film.id,
            target: person.id,
            value: 1
          })))
      }
    }))
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

  ticked () {
    this.link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    this.node
      .attr('cx', d => Math.max(this.radius, Math.min(this.width - this.radius, d.x))) // d.x)
      .attr('cy', d => Math.max(this.radius, Math.min(this.height - this.radius, d.y))) // d.y)

    this.textLabels
      .attr('dx', function dx (d) {
        return d.x - (this.getComputedTextLength() / 2)
      })
      .attr('dy', d => d.y - 15)
  }

  updateGraph () {
    const { data } = this.state
    const color = d3.scaleOrdinal(d3.schemeCategory20)

    this.link = this.link.data(data.links)

    this.link.exit().remove()
    this.link = this.link
      .enter()
      .append('line')
      .attr('class', 'link')
      .attr('stroke-width', d => d.value)
      .attr('stroke', 'gray')
      .merge(this.link)

    this.node = this.node.data(data.nodes)

    this.node.exit().remove()
    this.node = this.node
      .enter()
      .append('circle')
      .attr('class', 'node')
      .attr('r', 9)
      .call(d3.drag()
        .on('start', this.dragstarted)
        .on('drag', this.dragged)
        .on('end', this.dragended))
      .merge(this.node)
      .text(d => d.id)
      .attr('fill', d => color(d.group))

    this.textLabels = this.textLabels.data(data.nodes)

    this.textLabels.exit().remove()
    this.textLabels = this.textLabels
      .enter()
      .append('text')
      .attr('class', 'textLabels')
      .attr('font-family', 'sans-serif')
      .attr('font-size', '14px')
      .attr('fill', 'black')
      .merge(this.textLabels)
      .text(d => d.title)

    this.node.on('click', this.handleNodeClick)

    // this.node.append('title')
    //   .text(d => d.id)

    this.simulation
      .nodes(data.nodes)
      .on('tick', this.ticked)

    this.simulation.force('link')
      .links(data.links)

    this.simulation.alphaTarget(0.9).restart()
  }

  renderGraph () {
    this.svg = d3.select('svg')
    this.width = this.svg.attr('width')
    this.height = this.svg.attr('height')

    this.link = this.svg.append('g').selectAll('line')
    this.node = this.svg.append('g').selectAll('circle')
    this.textLabels = this.svg.append('g').selectAll('text')

    this.simulation = d3.forceSimulation()
      .force('link', d3.forceLink().distance(75).id(d => d.id))
      .force('charge', d3.forceManyBody().strength(() => -50))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))

    this.updateGraph()

    // this.showSearchPopup()
  }

  render () {
    const { searchVisible, searchOpen, node } = this.state
    return [
      <svg key="svg" width={window.innerWidth} height={window.innerHeight} />,
      searchVisible && (
        <div
          role="button"
          key="background"
          onClick={this.hideSearchPopup}
          onKeyDown={() => {}}
          className={cx(style.searchBackground, searchOpen && style.searchBackgroundOpen)}
          tabIndex="0"
        />
      ),
      searchVisible && (
        <div
          key="search"
          className={cx(style.search, searchOpen && style.searchOpen)}
          style={{ left: this.popupX, bottom: (window.innerHeight - this.popupY) + 20 }}
        >
          <SearchBar
            node={node}
            onDataUpdate={this.handleDataUpdate}
            onHideSearchPopup={this.hideSearchPopup}
          />
        </div>
      )
    ]
  }
}

export default Graph
