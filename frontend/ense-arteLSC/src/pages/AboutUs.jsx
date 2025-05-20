import Content from "../components/AboutUsComponents/Content"
import VerticalNavBar from "../components/VerticalNavBar"
const AboutUs = () => {
  return (
    <div  className="flex flex-row bg-[#F5F5F5] h-screen w-screen overflow-hidden  ">      
      <VerticalNavBar />
      <Content />
      
    </div>
  )
}

export default AboutUs
