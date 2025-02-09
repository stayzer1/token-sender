from web3 import Web3
import time

# Подключаемся к Sepolia testnet
w3 = Web3(Web3.HTTPProvider('https://unichain-sepolia-rpc.publicnode.com'))  # Замените на ваш Infura Project ID

# Конфигурация
SENDER_PRIVATE_KEY = 'example'  # Приватный ключ отправителя
AMOUNT_TO_SEND = 0.004  # Количество ETH для отправки (в ETH)
GAS_PRICE = w3.eth.gas_price
GAS_LIMIT = 21000  # Стандартный лимит газа для простой транзакции

def send_eth(to_address, amount_in_eth):
    try:
        # Получаем адрес отправителя из приватного ключа
        account = w3.eth.account.from_key(SENDER_PRIVATE_KEY)
        sender_address = account.address

        # Подготовка транзакции
        nonce = w3.eth.get_transaction_count(sender_address)
        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': w3.to_wei(amount_in_eth, 'ether'),
            'gas': GAS_LIMIT,
            'gasPrice': GAS_PRICE,
            'chainId': w3.eth.chain_id  # Chain ID для Sepolia
        }

        # Подписываем и отправляем транзакцию
        signed_txn = w3.eth.account.sign_transaction(transaction, SENDER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Ждем подтверждения транзакции
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print(f'Успешно отправлено {amount_in_eth} ETH на адрес {to_address}')
        return True

    except Exception as e:
        print(f'Ошибка при отправке на {to_address}: {str(e)}')
        return False

def main():
    # Читаем адреса из файла
    try:
        with open('wallets.txt', 'r') as file:
            private_keys = [line.strip() for line in file if line.strip()]

        # Отправляем ETH на каждый адрес
        for private_key in private_keys:
            recipient = w3.eth.account.from_key(private_key).address
            send_eth(recipient, AMOUNT_TO_SEND)
            time.sleep(2)  # Пауза между транзакциями

    except FileNotFoundError:
        print("Файл wallets.txt не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
