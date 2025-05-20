import VerticalNavBar from "../components/VerticalNavBar"
import Content from "../components/LearningComponents/Content"
const Learning = () => {
  return (
    <div className="flex flex-row bg-[#F5F5F5] h-screen w-screen overflow-hidden ">
      <VerticalNavBar />
      <Content />
    </div>
  )
}

export default Learning
