% Classical toral automorphism is mixing
% Nir Schwartz
% Last modified  21/02/2021
% We simulate the effect of applying a hyperbolic toral automorphism on
% a cluster of particles (see the attached image ell.rouge.png generated in
% tikZ) inside the fundamental unit square. The automorphism smears it
% along the unstable direction, illustrating the mixing property of the
% map. The code below is used to generate figure 1 in [S21].

% Erase previous vars etc.
clc;   
close all;
clear;
format long;
fontSize = 20;
rows=419;
columns=419;
% Read the image.
grayImage = imread('/home/schwarn/Dropbox/ell_rouge.png');
subplot(2, 2, 1);
% figure of the original unit square
imagesc(grayImage);
title('Original unit square','FontSize', 22,'Interpreter','latex');
% Iterate the toral map on the image. Here we used the DE map [[2,1],[3,2]]
% which is a canonical example for a classical toral hyperbolic
% automorphism which has quantum analogue.
iteration = 1;
oldScrambledImage = grayImage;
N = rows;
imwrite(oldScrambledImage, '/home/uname/iters/iteration.png');
while iteration <= 3
    set(gca,'xtick',[]);
    set(gca,'ytick',[]);
    frame = getframe(gcf);
	for row = 1 : rows
		for col = 1 : columns
			c = mod((2 * col) + row, N) + 1; % x coordinate
			r = mod((3 * col) + (2* row), N) + 1; % xi coordinate
			currentScrambledImage(row, col, :) = oldScrambledImage(r, c, :);
		end
	end
	
	% Display the current image.
	subplot(2, 2, iteration+1); 
    set(gca,'visible','off');
	imagesc(currentScrambledImage);
	title(['After applying $\gamma_0^',sprintf('%d',iteration),'$'], 'FontSize', 22,'Interpreter','latex');
	drawnow;
	oldScrambledImage = currentScrambledImage;
	iteration = iteration+1;
end
