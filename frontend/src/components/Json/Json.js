import React, { Component } from 'react';
import {Formik, Form, Field, FieldArray} from "formik";

let initialData = {
    "Event_id":"8477f080-8066-448d-9101-84579f3faf23",
    "Event_name":"string",
    "Event_Date":"1970-01-01T00:00:00+00:00",
    "Players":[{
        "Player_name":"qweqweqwe5",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"5e1d5965-6d8f-4de1-a6ab-8f77c2ca131c",
        "Points":3,
        "Sub_points":4
    },{
        "Player_name":"qweqweqwe",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"7b180db0-ccb6-4eba-9baa-272d22beaf50",
        "Points":0,
        "Sub_points":0
    },{
        "Player_name":"qweqweqwe3",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"7701faa7-767b-4be2-b5ef-7bd4c6f22a42",
        "Points":0,
        "Sub_points":0
    },{
        "Player_name":"qweqweqwe4",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"7bdbba66-4a0c-482d-98e7-a6f531d06d94",
        "Points":0,
        "Sub_points":0
    },{
        "Player_name":"qweqweqwe5",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"419980a5-dfb6-435d-a838-f5d44bf0593e",
        "Points":0,
        "Sub_points":0
    },{
        "Player_name":"qweqweqwe6",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"31cd8f92-5b33-4029-8d1e-7590b686ec5b",
        "Points":0,
        "Sub_points":0
    },{
        "Player_name":"qweqweqwe8",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"58b7c5d9-9790-4918-8319-630d64dc61d2",
        "Points":0,
        "Sub_points":0
    },{
        "Player_name":"qweqweqwe9",
        "Commander":"string",
        "Deck_link":"string",
        "Player_id":"91299d44-4055-4887-afc3-09ffdb73884c",
        "Points":0,
        "Sub_points":0
    }]};

const myRequest = new Request("http://localhost:8000/event-manager/get-full-event-data/8477f080-8066-448d-9101-84579f3faf23");

fetch(myRequest)
  .then(response => response.json())
  .then(data => {
    // initialData = data;
  });


export default class Json extends Component{

    render () {
        return (
        <div><h1>Our Event</h1>
        <Formik
        initialValues={initialData}
        onSubmit={values =>
            setTimeout(() => {
              alert(JSON.stringify(values, null, 2));
              }, 500)
        }
        render={({values}) => (
            <Form>
              <Field name="Event_id"/>
              <Field name="Event_name"/>
              <Field name="Event_Date"/>
              <FieldArray name="Players"
                          render={arrayHelpers => (
                              <div>
                                {values.Players && values.Players.length > 0 ? (
                                    values.Players.map((player, index) => (
                                        <div key={index}>
                                          <Field name={`Players.${index}.Player_name`}/>
                                          <Field name={`Players.${index}.Commander`}/>
                                          <Field name={`Players.${index}.Deck_link`}/>
                                          <Field name={`Players.${index}.Points`}/>
                                          <Field name={`Players.${index}.Sub_points`}/>
                                          <Field name={`Players.${index}.Has_autowin`}/>
                                          <Field name={`Players.${index}.Status`}/>
                                          <button type="button"
                                                  onClick={() => arrayHelpers.remove(index)}
                                                  >
                                            -
                                          </button>
                                          <button type="button"
                                                  onClick={() => arrayHelpers.insert(index)}
                                                  >
                                            +
                                          </button>
                                        </div>
                                    ))
                                ) : (<button>Nothing</button>) }
                                <div>
                                  <button type="submit">Sumbit</button>
                                </div>
                              </div>
                          )}
                          />
            </Form>
        )}/>
        </div>
        );
    }
}