import numpy as np

#Выручка в момент времени t при заданной сумме кредита Cкр
class CreditModel:
    def __init__(self, B0, Bpr, x, Ckr, gamma, alpha):
        self.B0 = B0  # Достигнутый уровень ежедневной выручки
        self.Bpr = Bpr  # Предельный уровень ежедневной выручки
        self.x = x  # Коэффициент для (Bpr - B0)
        self.Ckr = Ckr  # Сумма кредита
        self.gamma = gamma  # Коэффициент пропорциональности
        self.alpha = alpha  # Доля кредита на расходы
    
    def set_t(self, t):
        self.t = t  # Текущий день (например, день погашения)
    
    def set_periods_and_payments(self, t_pi, C_ps):
        self.t_pi = np.array(t_pi)  # Периоды погашения кредита
        self.C_ps = np.array(C_ps)  # Суммы погашения кредита
    
    def set_K_t(self, K_t):
        self.K_t = K_t  # Число периодов погашения кредита
    
    def calculate_B(self):
        # Вычисление суммы в скобках
        sum_t_pi = np.sum(self.t_pi[1:self.K_t])
        sum_C_ps = np.sum(self.C_ps[:self.K_t])
        
        # Вычисление выражения внутри exp
        exp_term = -self.gamma * (1 - self.alpha) * (self.Ckr * self.t - sum_t_pi - sum_C_ps)
        
        # Полная формула
        B_Ckr_t = self.B0 + (self.Bpr - self.B0) * self.x * (1 - np.exp(exp_term))
        
        return B_Ckr_t

if __name__ == "__main__":
    # Пример использования:
    credit_model = CreditModel(B0=100, Bpr=150, x=0.5, Ckr=50000, gamma=0.1, alpha=0.3)
    credit_model.set_t(30)  # Установить текущий день
    credit_model.set_periods_and_payments(t_pi=[10, 20, 30, 40, 50], C_ps=[1000, 2000, 3000, 4000, 5000])
    credit_model.set_K_t(5)  # Установить число периодов погашения кредита

    result = credit_model.calculate_B()
    print("B(Ckr, t) =", result)
