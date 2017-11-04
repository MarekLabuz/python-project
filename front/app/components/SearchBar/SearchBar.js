import React, { Component } from 'react'
// import PropTypes from 'prop-types'
import debounce from 'lodash/debounce'

// import Map from '../../map'
import Loader from '../Loader/Loader'
// import API from '../../api'

import style from './SearchBar.scss'

const mockData = [
  { id: 1, title: 'Mother' },
  { id: 2, title: 'Bałwanek' },
  { id: 3, title: 'Prometeusz' },
  { id: 4, title: 'Makbet' }
]

const api = () => new Promise(resolve => setTimeout(() => resolve(mockData), 500))

class SearchBar extends Component {
  constructor () {
    super()

    this.state = {
      loading: false,
      data: []
    }

    this.handleInput = this.handleInput.bind(this)
    this.handleSelect = this.handleSelect.bind(this)
    this.search = debounce(this.search.bind(this), 250)
  }

  search (text, timestamp) {
    api()
      .then((data) => {
        if (timestamp === this.inputTimestamp) {
          this.setState({
            loading: false,
            data
          })
        }
      })
  }

  handleInput (e) {
    this.inputTimestamp = +new Date()
    this.setState({
      loading: true
    })
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

  handleSelect (text) {
    console.log(text)
  }

  render () {
    const { data, loading } = this.state
    return (
      <div className={style.container}>
        <input
          className={style.input}
          onInput={this.handleInput}
          placeholder="Enter movie title"
        />
        {
          data.length || loading
            ? (
              <div className={style.results}>
                <Loader condition={loading}>
                  <ul>
                    {data.map(v => (
                      <li key={v.id}>
                        <div
                          role="button"
                          onClick={() => this.handleSelect(v.title)}
                          onKeyDown={e => e.keyCode === 13 && this.handleSelect(v.title)}
                          tabIndex="0"
                        >
                          {v.title}
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

export default SearchBar
