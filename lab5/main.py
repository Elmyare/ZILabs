from Server import ServerModule
from Client import ClientModule

def main():
    server = ServerModule()
    clients = [
        ClientModule(server, "Alice"),
        ClientModule(server, "Bob"),
        ClientModule(server, "Charlie"),
    ]

    # Голосование
    clients[0].vote(ServerModule.VoteOption.YES)
    clients[1].vote(ServerModule.VoteOption.NO)
    clients[2].vote(ServerModule.VoteOption.ABSTAIN)

    # Подсчет результатов
    server.voting_results()

if __name__ == "__main__":
    main()