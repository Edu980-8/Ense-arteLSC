import React from 'react'
import VerticalNavBar from '../VerticalNavBar'
import Points from './Points'

const DashboardComponent = () => {
  return (
    <div className="w-full  h-[100svh] flex">
      <VerticalNavBar /> 
      <Points />
    </div>
  )
}

export default DashboardComponent
