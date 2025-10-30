"use client"
import React, {useState} from 'react';
import axios from 'axios';
import { State, City , IState, ICity} from 'country-state-city';

const MgnregaData: React.FC = () => {

    const [state, setState] = useState<string>("")
    const [district, setDistrict] = useState<string>("")
    // const [year, setYear] = useState<string>("")
    const [data, setData] = useState<any>(null)
    const [loading, setLoading] = useState<boolean>(false)

    // this variable takes states in an array in the format if IStates that comes in the lib
    const indianStates: IState[] = State.getStatesOfCountry("IN");
    const districtsInState: ICity[]= state ? City.getCitiesOfState("IN",state): [];

    const fetchData = async ()=>{
        // fetch data from backend
        console.log(`fetch data function called`)
        setLoading(true);

        const stateName = indianStates.find(s => s.isoCode === state)?.name.toUpperCase();
        const districtName = district.toUpperCase();
        console.log(`state name: ${stateName}`)
        console.log(`district name: ${districtName}`)
        
        await axios.get("http://localhost:8000/fetch_api_data", {
            params:{
                state_name: stateName,
                district_name: districtName
            }
        }).then((res: { data: { data: any; }; })=>{
            console.log(`state:`, stateName);
            console.log(`district`, district)
            console.log("backend response ", res.data);
            setData(res.data);

        }).catch((err: any)=>{
            console.log("error in fetching data from backend", err);

        }).finally(()=>{
            setLoading(false);
        })

    }

    return(
        
       <div>
            <h1>Mgnrega Website</h1>
                <select
                    value={state}
                    onChange={(e)=>{
                        setState(e.target.value);
                        setDistrict("");
                    }}
                >
                    <option value="">Select state</option>
                    {indianStates.map((s)=>(
                        <option key={s.isoCode} value={s.isoCode}>
                            {s.name}
                        </option>
                    ))}
                </select>

                <select
                    value={district}
                    onChange={(e)=>(
                        setDistrict(e.target.value))}
                        disabled={!state}
                >
                    <option value="">Select District</option>
                    {districtsInState.map((d)=>(
                        <option key={d.name} value={d.name}>
                            {d.name}
                        </option>
                    ))}
                </select>

                <button
                    onClick={fetchData} disabled={!state || loading}
                >
                    {loading ? "Loading..." : "Fetch Data"}
                </button>

                {data && ( 
                    <pre style={{ textAlign: "left" }}> 
                        {JSON.stringify(data.data, null, 2)} 
                    </pre>
                 )}

       </div>
    
        
    )
}

export default MgnregaData;