import { Copyright } from '@mui/icons-material';

export default function Footer() {
    return (
        <footer className='mt-20 w-full px-5 py-6 bg-zinc-300 text-center text-white'>
            <p><Copyright sx={{ fontSize: 20 }}/> Copyright CentraleSupélec</p>
        </footer>
    );
}