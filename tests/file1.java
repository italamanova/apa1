package package2;

import package1.Panel;
import package3.F16eXXXtreeeme;
import package3.RailgunAmmo;

public class FlightSim {
    public static void bla(){
    }
	public static void main(String[] args) throws InterruptedException {
		Panel p = new Panel(60);

		F16eXXXtreeeme f16 = new F16eXXXtreeeme(p);
		RailgunAmmo ammo = new RailgunAmmo(f16, p);
		while (true) {
			for (int i = 0; i <= p.size(); i++) {
				f16.moveRight();
				f16.redraw();
				for (int bulletSpeedUp = 0; bulletSpeedUp < 4; bulletSpeedUp++) {
					ammo.animateRight();
				}
			}
			f16.resetOffset();
			ammo.resetOffset();
		}
	}

}