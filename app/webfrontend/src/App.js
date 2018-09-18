import React from 'react'
import axios, { post } from 'axios';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state ={
      file:null,
      //isuser:false,
      user_id:null,
      //doctor_id:null
    }
    this.onFormSubmit = this.onFormSubmit.bind(this)
    this.onChange = this.onChange.bind(this)
    this.fileUpload = this.fileUpload.bind(this)
    this.userId=this.userId.bind(this)
  }
  onFormSubmit(e){
    e.preventDefault() // Stop form submit
    this.fileUpload(this.state.file).then((response)=>{
      console.log(response.data);
    })
  }
  onChange(e) {
    this.setState({file:e.target.files[0]})
  }
  userId(e) {
      console.log(e.target.value)
      this.setState({user_id:e.target.value})
  }
  fileUpload(file){
    const url = 'http://localhost:5000/user_profile';
    const formData = new FormData();
    formData.append('file',file)
    formData.append('doctor_id',"doctor_id")
    console.log(formData)
    const config = {
        headers: {
            'content-type': 'multipart/form-data'
        }
    }
    console.log(formData.get('doctor_id'))
    return  post(url, formData,config)
  }

  render() {
    return (
      <form onSubmit={this.onFormSubmit}>
        <h1>File Upload</h1>
        <input type="file" onChange={this.onChange} />
        <button type="submit">Upload</button>
        <h1>userid</h1>
        <input type="text" onChange={this.userId}/>
      </form>
   )
  }
}



export default App