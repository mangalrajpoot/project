import {useState} from 'react'
function Form()
{


    let [formdata,setFormdata]=useState({
        name:'',
        email:'',
        gender:'',
        course:'',
        country:'',
    })
    let [errors,setErrors]=useState({
        name:'',
        email:'',
        gender:'',
        course:'',
        country:'', 
    })
    let countries=['india','china','america']

    let validateForm=()=>
    {
        let valid=true;
        const newErrors={...errors};

        if(formdata.name==='')
        {
newErrors.name='Name is required'
valid=false;
        }
        else 
        {
        newErrors.name= ""

        }
if(!formdata.email.match(/^\w+@\w+\.\w+$/))
{
    newErrors.email='Invalid Email Address'
    valid=false;
}
else 
{
    newErrors.email=''
    valid=true;
}
if(formdata.gender==='')
{
    newErrors.gender='Please select a gender';
    valid=false;
}
else
{
    newErrors.gender='';
}
if (formdata.course.length === 0) {
    newErrors.course = 'Please select at least one course';
    valid = false;
} else {
    newErrors.course = '';
}


if(formdata.country==='')
{
    newErrors.country='Please select a country'
    valid=false;
}
else 
{
    newErrors.country=''
}
setErrors(newErrors)
return valid;


    }
let handleSubmit=(e)=>
{
    e.preventDefault();
    if(validateForm())
    {
console.log('Form Submitted',formdata)
    }
}

let handleInputChange=(e)=>
{
    let {name,value,type,checked}=e.target;
    let newValue=type==='checkbox'?checked:value;
    setFormdata(
        {
            ...formdata,
            [name]:newValue,
        }
    )
}

    return (
        <>
        <h1>Form Validation in React</h1>
        <form onSubmit={handleSubmit}>


<input type='text' onChange={handleInputChange} name='name'></input><br/> 
        <span className='error4'>{errors.name}</span><br/>      
<input type='text' onChange={handleInputChange} name='email'/> <br/> 
        <span className='error5'>{errors.email}</span><br/>    
<label>Gender : </label>
<input type='radio' name='gender' onChange={handleInputChange} value='male'/>Male
<input type='radio' name='gender' onChange={handleInputChange} value='female'/>Female <br/>
<span className='error1'>{errors.gender}</span><br/>
<label>Course</label>
<input type='checkbox' value='html' onChange={handleInputChange} name='course'/>HTML
<input type='checkbox' value='css' onChange={handleInputChange} name='course'/><br/>CSS <br/>
<span className='error2'>{errors.course}</span><br/>
<label>Country</label>

<select name='country' onChange={handleInputChange}>
    <option>Select a countty</option>
    {countries.map((country)=>
    (

        <option key={country}  value={country}>{country}</option>
    )

    )}
   
    

 

</select><br/>
<span className='error3'>{errors.country}</span><br/>

<input type='submit'/>





        </form>
        
        
        
        </>
    )
}
export default Form;