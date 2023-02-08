from ic.identity import Identity
from ic.client import Client
from ic.agent import Agent
from ic.principal import AccountIdentifier
from ic.candid import encode, decode, Types
import time
import asyncio
import tokenIdentifier as ti
import pandas as pd

class MainClient:
    # 設定
    with open('identity_plug.pem','r') as f:
        private_key_1 = f.read()
    client = Client(url = "https://ic0.app")
    agent = Agent(Identity.from_pem(private_key_1), client)
    canistar = 'skjpp-haaaa-aaaae-qac7q-cai' #ここにcanistarを入れる
    #0.1とかでも動きますが念のため
    sleeptime = 0.2

    def __init__(self):
        loop = asyncio.get_event_loop()
        tasks = [
            self.main()
            ]
        loop.run_until_complete(asyncio.wait(tasks))

    async def main(self):
        #WLにprincipalをlistで追加
        WL = pd.read_csv("foo.csv").values.tolist()
        # WL =[  ]
        #indexを0から変化させていくために入れました。
        index = -1
                
        for to_principal in WL:
            #principalをアドレスに変換
            self.to_address = AccountIdentifier.new(to_principal)._hash.hex()
            index += 1

            token_id = ti.tokenIdentifier(self.canistar,index)
            asyncio.create_task(self.transfer(token_id))
            await asyncio.sleep(self.sleeptime)
        #txの時間がまちまちなため待った方が良いようです。
        time.sleep(10)

    async def transfer(self,token_id):
        #txを発火
        transfer = await self.agent.update_raw_async(self.canistar, 'transfer', self.nftTransfer(token_id))
        print('成功！',transfer)
        return

    def nftTransfer(self,token_id): #apiの引数を入力
        print(token_id,self.to_address,self.myaddress)

        types = Types.Record({
                'to':Types.Variant({'address':Types.Text}),
                'token': Types.Text,
                'notify':Types.Bool,
                'from':Types.Variant({'address':Types.Text}),
                'memo':Types.Vec(Types.Nat8),
                'subaccount':Types.Opt(Types.Vec(Types.Nat8)),
                'amount':Types.Nat})

        values = {
                'to':{'address':self.to_address},
                'token': token_id,
                'notify':False,
                'from':{'address':self.myaddress},
                'memo':"",
                'subaccount':[],
                'amount':1
        }

        params = [{'type': types, 'value': values}]

        return encode(params)

if __name__ == "__main__":
    MainClient()
