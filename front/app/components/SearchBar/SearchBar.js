import React, { Component } from 'react'
import PropTypes from 'prop-types'
import debounce from 'lodash/debounce'

// import Map from '../../map'
import Loader from '../Loader/Loader'
// import API from '../../api'

import style from './SearchBar.scss'

// const mockData = [
//   { id: 1, title: 'Mother' },
//   { id: 2, title: 'Bałwanek' },
//   { id: 3, title: 'Prometeusz' },
//   { id: 4, title: 'Makbet' }
// ]

const api = {
  moviesByQuery: query => fetch(`http://localhost:5000/movies?query=${encodeURI(query)}`),
  moviesByActor: id => fetch(`http://localhost:5000/movies-actor?id=${encodeURI(id)}`)
}

class SearchBar extends Component {
  constructor (props) {
    super()

    this.state = {
      loading: props.node && props.node.group === 'person',
      data: []
    }

    this.handleInput = this.handleInput.bind(this)
    this.handleSelect = this.handleSelect.bind(this)
    this.search = debounce(this.search.bind(this), 500)
  }

  componentDidMount () {
    const { node } = this.props
    if (node.group === 'person') {
      api.moviesByActor(node.id)
        .then(data => data.json())
        .then(({ cast }) => {
          this.setState({
            loading: false,
            data: cast.slice(0, 10)
          })
        })
    }
  }

  search (text, timestamp) {
    api.moviesByQuery(text)
      .then(data => data.json())
      .then(({ results }) => {
        if (timestamp === this.inputTimestamp) {
          this.setState({
            loading: false,
            data: results.slice(0, 10)
          })
        }
      })
  }

  handleInput (e) {
    this.inputTimestamp = +new Date()
    this.setState({ loading: true })
    const text = e.target.value
    if (text.length) {
      this.search(text, this.inputTimestamp)
    } else {
      this.setState({
        loading: false,
        data: []
      })
    }
  }

  handleSelect (id) {
    const { onHideSearchPopup, onDataUpdate, node } = this.props
    onHideSearchPopup()
    fetch(`http://localhost:5000/movie?id=${id}&actor_id=${(node && node.id) || ''}`)
      .then(data => data.json())
      .then(film => onDataUpdate(film))
      .catch(console.log)
  }

  render () {
    const { data, loading } = this.state
    const { node } = this.props
    return (
      <div className={style.container}>
        {node.group === 'mock' && (
          <input
            className={style.input}
            onInput={this.handleInput}
            placeholder="Enter movie title"
          />
        )}
        {
          data.length || loading
            ? (
              <div className={style.results}>
                <Loader condition={loading}>
                  <ul>
                    {data.map(v => (
                      <li key={v.id}>
                        <div
                          className={style.item}
                          role="button"
                          onClick={() => this.handleSelect(v.id)}
                          onKeyDown={e => e.keyCode === 13 && this.handleSelect(v.id)}
                          tabIndex="0"
                        >
                          <span>{v.title}</span>
                          <span>{v.release_date.split('-')[0]}</span>
                        </div>
                      </li>
                    ))}
                  </ul>
                </Loader>
              </div>
            )
            : null
        }
      </div>
    )
  }
}

SearchBar.propTypes = {
  node: PropTypes.object.isRequired,
  onHideSearchPopup: PropTypes.func.isRequired,
  onDataUpdate: PropTypes.func.isRequired
}

export default SearchBar
