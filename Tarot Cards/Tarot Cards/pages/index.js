
import Head from 'next/head';
import MotherProtocol from '../components/MotherProtocol';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Butterfly Chat</title>
      </Head>
      <MotherProtocol />
    </div>
  );
}
