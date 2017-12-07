import React from 'react'
import PropTypes from 'prop-types'

import style from './Loader.scss'

function Loading () {
  return (
    <div className={style.container}>
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
      <div className={style.arm} />
    </div>
  )
}

function Loader ({ condition, children }) {
  return (
    condition
      ? <div style={{ minHeight: 100 }}><Loading /></div>
      : children
  )
}

Loader.propTypes = {
  condition: PropTypes.bool.isRequired,
  children: PropTypes.node.isRequired
}

export default Loader
