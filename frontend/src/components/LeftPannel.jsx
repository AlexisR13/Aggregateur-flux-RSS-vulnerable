function LeftButton(props) {
  return(
    <li>
      <button className={'my-2 w-full py-1 px-3 border ' + (props.isActive?'bg-slate-300':'')}
        onClick={props.onClick}>
        {props.text}
      </button>
    </li>
  )
}


export default function LeftPannel(props) {
  return (
    <div className='h-screen mx-10 pr-6 border-r border-r-slate-900'>
        <ul className="w-max">
            <LeftButton 
            text='Home' 
            isActive={props.pannelSelected==='home'}
            onClick={() => props.setPannelSelected('home')}/>
            <LeftButton 
            text='Tous les articles'
            isActive={props.pannelSelected==='all'}
            onClick={() => props.setPannelSelected('all')}/>
            <LeftButton 
            text='Voir les feeds'
            isActive={props.pannelSelected==='feeds'}
            onClick={() => props.setPannelSelected('feeds')}/>
        </ul>
    </div>
    );
}
